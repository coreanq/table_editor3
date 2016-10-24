import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp, Qt, QItemSelectionModel, QStringListModel
import mainwindow_ui 
import view_delegate as cbd 
import view_key_eater as ve
import column_info as ci
import read_data as rd
import util


class MainWindow(QMainWindow, mainwindow_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.model_group = QStandardItemModel(self)
        self.model_proxy_group = QSortFilterProxyModel(self)

        self.model_parameters = QStandardItemModel(self)
        self.model_proxy_parameters = QSortFilterProxyModel(self)
        
        self.model_msg_info = QStandardItemModel(self)
        self.model_proxy_msg_info = QSortFilterProxyModel(self)

        self.model_msg_values = QStandardItemModel(self)
        self.model_proxy_msg_values = QSortFilterProxyModel(self)
        
        self.model_vari = QStandardItemModel(self)
        self.model_proxy_vari = QSortFilterProxyModel(self)
        
        self.model_title = QStandardItemModel()
        self.model_proxy_title = QSortFilterProxyModel(self)

        #delegate 선언 
        self.delegate_parameters_view = cbd.ViewDelegate(self)
        self.delegate_msg_view = cbd.ViewDelegate(self)
        self.delegate_group_view = cbd.ViewDelegate(self)
        
        self.model_kpd_para_unit = QStandardItemModel()

        self.readDataFromFile() 
        self.initView()
        self.initDelegate()
        self.createConnection()
        pass

    def createConnection(self):
        self.viewGroup.clicked.connect(self.onViewGroupClicked)  
        self.viewMsgInfo.clicked.connect(self.onViewMsgInfoClicked)
        
        # ctrl + c, ctrl + v, insert, delete 누를 시 
        parameter_view_eater = ve.ViewKeyEater(self)
        self.viewParameter.installEventFilter(parameter_view_eater)
        parameter_view_eater.sig_copy_clicked.connect(self.onParameterViewCopyed)
        parameter_view_eater.sig_paste_clicked.connect(self.onParameterViewPasted)
        parameter_view_eater.sig_insert_clicked.connect(self.onParameterViewInserted)
        parameter_view_eater.sig_delete_clicked.connect(self.onParameterViewDeleted)

        group_view_eater = ve.ViewKeyEater(self)
        self.viewGroup.installEventFilter(group_view_eater)
        group_view_eater.sig_copy_clicked.connect(self.onGroupViewCopyed)
        group_view_eater.sig_paste_clicked.connect(self.onGroupViewPasted)
        group_view_eater.sig_insert_clicked.connect(self.onGroupViewInserted)
        group_view_eater.sig_delete_clicked.connect(self.onGroupViewDeleted)

        msg_info_view_eater = ve.ViewKeyEater(self)
        self.viewMsgInfo.installEventFilter(msg_info_view_eater)
        msg_info_view_eater.sig_copy_clicked.connect(self.onMsgInfoViewCopyed)
        msg_info_view_eater.sig_paste_clicked.connect(self.onMsgInfoViewPasted)
        msg_info_view_eater.sig_insert_clicked.connect(self.onMsgInfoViewInserted)
        msg_info_view_eater.sig_delete_clicked.connect(self.onMsgInfoViewDeleted)

        msg_value_view_eater = ve.ViewKeyEater(self)
        self.viewMsgValue.installEventFilter(msg_value_view_eater)
        msg_value_view_eater.sig_copy_clicked.connect(self.onMsgValueViewCopyed)
        msg_value_view_eater.sig_paste_clicked.connect(self.onMsgValueViewPasted)
        msg_value_view_eater.sig_insert_clicked.connect(self.onMsgValueViewInserted)
        msg_value_view_eater.sig_delete_clicked.connect(self.onMsgValueViewDeleted)

        # parametere view  더블 클릭시 unit의 msg combobox 내용을 변경하기 위함  
        self.viewParameter.doubleClicked.connect(self.onViewParameterDoubleClicked)
        self.model_parameters.dataChanged.connect(self.onModelParameterDataChanged)
        pass

    def initView(self):
        view_list = [self.viewGroup,  
                    self.viewParameter, self.viewMsgInfo, 
                    self.viewMsgValue, self.viewVariable, 
                    self.viewTitle]

        # group view init 
        self.model_proxy_group.setSourceModel(self.model_group)
        self.viewGroup.setModel(self.model_proxy_group)
        self.model_group.setHorizontalHeaderLabels(ci.group_col_info() )

        # prameter view init
        self.model_proxy_parameters.setSourceModel(self.model_parameters)
        self.viewParameter.setModel(self.model_proxy_parameters) 
        self.model_parameters.setHorizontalHeaderLabels(ci.para_col_info_for_view() )
        self.viewParameter.setColumnHidden( ci.para_col_info_for_view().index('Group'), True)
       
        # msg info view init 
        self.model_proxy_msg_info.setSourceModel(self.model_msg_info) 
        self.viewMsgInfo.setModel(self.model_proxy_msg_info)
        self.model_msg_info.setHorizontalHeaderLabels(ci.msg_info_col_info() )

        # msg value view init 
        self.model_proxy_msg_values.setSourceModel(self.model_msg_values)
        self.viewMsgValue.setModel(self.model_proxy_msg_values)
        self.model_msg_values.setHorizontalHeaderLabels(ci.msg_values_col_info())
        self.viewMsgValue.setColumnHidden(ci.msg_values_col_info().index('MsgName'), True)
        self.viewMsgValue.setColumnHidden(ci.msg_values_col_info().index('MsgInfo'), True)
        
        # vari view init
        self.model_proxy_vari.setSourceModel(self.model_vari)
        self.viewVariable.setModel(self.model_proxy_vari)
        self.model_vari.setHorizontalHeaderLabels(ci.variable_col_info() )
        
        # title view init 
        self.model_proxy_title.setSourceModel(self.model_title)
        self.viewTitle.setModel(self.model_proxy_title)
        self.model_title.setHorizontalHeaderLabels(ci.title_col_info() )

        # filter 값을 이상한 값으로 넣어 처음에는 아무 리스트가 안나타나게 함 
        proxy_list = [  self.model_proxy_msg_values, self.model_proxy_parameters, 
                        # self.model_proxy_title, self.model_proxy_vari  
        ]  
        for proxy in proxy_list:
            regx = QRegExp("!@#$") 
            proxy.setFilterKeyColumn(0)
            proxy.setFilterRegExp(regx)

        # 모든 view 기본 설정  
        for item in view_list:
            item.setAlternatingRowColors(True)
            item.setSelectionBehavior(QAbstractItemView.SelectRows)
            item.setSelectionMode(QAbstractItemView.SingleSelection)
            horizontalHeaderView  = item.horizontalHeader()
            horizontalHeaderView.setStretchLastSection(True)
            horizontalHeaderView.setSectionResizeMode(QHeaderView.ResizeToContents)
            # row drag & drop 을 위해서는 headerView 를 설정해야함 view 자체에서는 안됨 
            verticalHeaderView = item.verticalHeader()
            verticalHeaderView.setSectionsMovable(True)
            verticalHeaderView.setDragEnabled(True)
            verticalHeaderView.setDragDropMode(QAbstractItemView.InternalMove)

    def setCmbDelegateAttribute(self, model, view, delegate, columns = [], editable = False, width = 0):
        for col_index in columns:
            delegate.setEditable(col_index,  editable ) 
            delegate.setEditorType(col_index, 'combobox')
            delegate.setModel(col_index, model)
            view.setItemDelegateForColumn(col_index, delegate)
            if( width != 0 ):
                header_view = view.horizontalHeader()
                header_view.setSectionResizeMode(col_index, QHeaderView.Fixed)
                view.setColumnWidth(col_index, width )
        pass 
        
    def initDelegate(self):
        # delegate 는 하나만 사용 가능 
        # parameters view delegate 설정 
        model = self.model_title
        view = self.viewParameter
        delegate = self.delegate_parameters_view
        col_info = ci.para_col_info_for_view()
        col_index = col_info.index('Code TITLE')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], width = 150)

        model = self.model_kpd_para_unit
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_index = col_info.index('단위')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], editable = False,  width = 150)

        model = self.model_vari
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ col_info.index('Para 변수'), 
                        col_info.index('최대값'),
                        col_info.index('최소값'),
                        col_info.index('보임변수')
        ]
        self.setCmbDelegateAttribute(model, view, delegate, col_indexes, editable = True,  width = 150)

        model = QStringListModel( ['True', 'False']) 
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ col_info.index('통신쓰기금지'), 
                        col_info.index('읽기전용'),
                        col_info.index('운전중변경불가'),
                        col_info.index('0 입력가능')
        ]
        self.setCmbDelegateAttribute(model, view, delegate, col_indexes )

        # msg view delegate 설정 
        model = self.model_title
        view  = self.viewMsgValue
        delegate = self.delegate_msg_view  
        col_info = ci.msg_values_col_info()
        col_index = col_info.index('TitleIndex')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], width = 150)

        # group view delegate 설정 
        model = self.model_vari
        view  = self.viewGroup
        delegate = self.delegate_group_view  
        col_info = ci.group_col_info()
        col_index = col_info.index('Hidden Vari')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], editable = True , width = 150)
        pass
       
    # unit 선택에 따라서 수시로 변하기 때문에 따로 함수로 만들어 줌 
    # unit 컬럼이나 form/msg 컬럼을 더블 클릭하는 두개의 경우에 대해서 동작해야함 
    def initParameterMsgDelegate(self, proxy_index): 
        col_info = ci.para_col_info_for_view()
        model = self.model_parameters
        proxy_model = self.model_proxy_parameters
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        delegate_model = None
        row_source_index = proxy_model.mapToSource(proxy_index)


        unit_col_index = col_info.index('단위')
        form_msg_col_index = col_info.index('폼메시지')

        unit_data = model.item(row_source_index.row() , unit_col_index).text()

        if( unit_data == 'U_DATAMSG' or unit_data == 'U_RPM_CHG_DATAMSG'):
            delegate_model = self.model_msg_info
        elif( unit_data == 'U_HZ_RPM'):
            delegate_model = ci.unit_with_msg()[unit_data]
        elif( unit_data == 'U_B'):
            delegate_model = ci.unit_with_msg()[unit_data]
        else: 
            delegate_model = ci.unit_with_msg()['Other']
        self.setCmbDelegateAttribute(delegate_model, view, delegate, [form_msg_col_index], editable = False,  width = 150)

        pass 


    @pyqtSlot(QModelIndex)
    def onViewGroupClicked(self, index):
        # print(util.whoami() )
        row = index.row()
        grp_name = self.model_group.item(row, 0 ).text() 
        regx = QRegExp(grp_name.strip()) 
        self.model_proxy_parameters.setFilterKeyColumn(0)
        self.model_proxy_parameters.setFilterRegExp(regx)
        # 클립 보드 삭제 
        clipboard = QApplication.clipboard()
        clipboard.clear()
        pass
     
    @pyqtSlot(QModelIndex)
    def onViewMsgInfoClicked(self, index):
        # print(util.whoami() )
        row = index.row()
        msg_name = self.model_msg_info.item(row, 0).text()
        regx = QRegExp(msg_name.strip() )
        self.model_proxy_msg_values.setFilterKeyColumn(0)
        self.model_proxy_msg_values.setFilterRegExp(regx)
         
        pass
    def searchTitlefromEnumName(self, enumName):
        col_info = ci.title_col_info()
        items = self.model_title.findItems(enumName, column =col_info.index('Enum 이름'))
        for item in items:
            row = item.row()
            return self.model_title.item(row, col_info.index('Title')).text() 
        return ("Error")
        pass

    # read_para_table 에서는 단순히 파일을 파싱해서 올려주는 역할만 하고 
    # 올라온 데이터에 대한 수정은 상위단에서 수행하도록 함 
    def readDataFromFile(self):
        target_dir = r'D:\download\1'
            # print(root, directories, filenames)
        for filename in rd.parsing_files:
            file_path = target_dir + os.sep + filename 
            if( os.path.exists(file_path) ):
                contents = ""
                with open(file_path, 'r', encoding='utf8') as f:
                    contents = f.read()
                if(filename.lower() == rd.KPD_PARA_TABLE_SRC_FILE ):
                    for items in rd.read_para_table(contents):
                        col_info = ci.para_col_info_for_file()
                        arg = items[col_info.index('Attribute')] 
                        attribute  = int(arg, 16)
                        comm_write_protect  = 'False' 
                        read_only = 'False'
                        no_modify_on_run = 'False'
                        is_insert_zero_possible = 'False'
                        if( attribute & 0x0040 ):
                            comm_write_protect = 'True'
                        if( attribute & 0x0008 ):
                            read_only = 'True'
                        if( attribute & 0x0010 ):
                            no_modify_on_run = 'True'
                        if( attribute & 0x0020 ):
                            is_insert_zero_possible = 'True'
                            
                        title = self.searchTitlefromEnumName(items[col_info.index('TitleIndex')])
                        
                        try : 
                            view_col_list = [ items[col_info.index('Group')],  
                                            items[col_info.index('Code#')],  
                                            title, 
                                            items[col_info.index('AtValue')], 
                                            items[col_info.index('ParaVari')],
                                            items[col_info.index('KpdFunc')],
                                            items[col_info.index('DefaultVal')],
                                            items[col_info.index('MaxVal')],
                                            items[col_info.index('MinVal')],
                                            items[col_info.index('Msg')].replace('MSG_', ''),
                                            items[col_info.index('Unit')],
                                            comm_write_protect,
                                            read_only, 
                                            no_modify_on_run,
                                            is_insert_zero_possible,
                                            items[col_info.index('ShowVari')],
                                            items[col_info.index('ShowVal')],
                                            '', # TODO: eep주소 
                                            '', # TODO: 통신주소 
                                            items[col_info.index('MaxEDS')],
                                            items[col_info.index('MinEDS')],
                                            items[col_info.index('Comment')]
                            ]
                            self.addRowToModel(self.model_parameters, view_col_list)
                        except IndexError:
                            print('error occur')
                            print(items)
                        
                    for items in rd.read_grp_info(contents):
                        self.addRowToModel(self.model_group, items)
                        pass
                    pass
                elif( filename.lower() == rd.KPD_PARA_MSG_SRC_FILE):
                    msg_list = [] 
                    col_info = ci.msg_values_col_info()
                    title_index = col_info.index('TitleIndex')
                    for items in rd.read_para_msg(contents):
                        msg_info = [items[col_info.index('MsgName')], items[col_info.index('MsgInfo')]] 

                        if( msg_info not in msg_list ):
                            msg_list.append(msg_info) 
                        title = self.searchTitlefromEnumName(items[title_index])
                        insert_list = *items[:title_index], title,  *items[title_index +1: ]
                        self.addRowToModel(self.model_msg_values, insert_list)
                        pass

                    for item in msg_list:
                        self.addRowToModel(self.model_msg_info, item)
                        
                elif( filename.lower() == rd.KPD_PARA_VARI_HEADER_FILE):
                    for items in rd.read_kpd_para_vari(contents):
                        self.addRowToModel(self.model_vari, items)
                    pass
                elif ( filename.lower() == rd.KPD_BASIC_TITLE_SRC_FILE):
                    for items in rd.read_basic_title(contents):
                        # 항상 add title 보다 앞서야 하므로 
                        self.addRowToModel(self.model_title, items, editing = False)
                    pass
                elif ( filename.lower() == rd.KPD_PARA_STRUCT_UNIT_HEADER_FILE):
                    for items in rd.read_kpd_para_struct_unit(contents):
                        for item in items:
                            self.model_kpd_para_unit.appendRow(QStandardItem(item))

                elif ( filename.lower() == rd.KPD_ADD_TITLE_SRC_FILE ):
                    for items in rd.read_add_title(contents):
                        self.addRowToModel(self.model_title, items)
                pass
        pass
        
    def addRowToModel(self, model, data_list, editing = True):
        item_list = []
        for data in data_list:
            item = QStandardItem(data)
            if( not editing ):
                item.setBackground(QColor(Qt.darkGray) )
            item.setEditable(editing)
            item_list.append(item)            
        model.appendRow(item_list)
        pass

    def insertRowToModel(self, model, datas, insert_index, editing = True):
        item_list = []
        for data in datas:
            item = QStandardItem(data)
            item.setEditable(editing)
            item_list.append(item)

        # rowCount 는 1부터 시작 insert_index 는 0 부터  시작 
        if( insert_index+ 1 >= model.rowCount() ):
            model.appendRow(item_list)
            pass
        else :
            model.insertRow(insert_index + 1, item_list)
            pass
        pass

    @pyqtSlot(QModelIndex)
    def onViewParameterDoubleClicked(self,index):
        self.initParameterMsgDelegate(index) 
        pass

    @pyqtSlot(QModelIndex, QModelIndex)
    def onModelParameterDataChanged(self, topLeft, bottomRight):
        # unit 의 데이터가 변한 경우 Msg 에 띄울 combobox list 가 변해야 하므로 
        col_info = ci.para_col_info_for_view()
        top_row_index = topLeft.row()
        top_col_index = topLeft.column()
        bottom_row_index = topLeft.row()
        bottom_col_index = topLeft.column()
          
        pass 
    

    def viewRowCopy(self, view):
        clipboard = QApplication.clipboard()
        view_model = view.model()
        selection_model = view.selectionModel()
        row_indexes = selection_model.selectedRows()
        rows = [] 

        # 한줄만 선택 
        for row_index in row_indexes:
            row_data = ','.join(view_model.data(row_index.sibling(row_index.row(), column)) for column in range(view_model.columnCount() )) 
            rows.append(row_data)

        clipboard.setText( '\n'.join(rows))
        # print('\n'.join(rows))
        pass

    def viewRowPaste(self, view, source_model):
        clipboard = QApplication.clipboard()
        view_model = view.model() 
        selection_model = view.selectionModel()
        row_indexes = selection_model.selectedRows()

        # 한줄만 선택 
        for row_index in row_indexes:
            source_index = None
            if( source_model == view_model ):
                source_index = row_index
            else :
                source_index = view_model.mapToSource( row_index ) 
            insert_row = source_index.row() 
            for row in clipboard.text().split('\n'):
                row_items = row.split(',')
                self.insertRowToModel(source_model, row_items, insert_row)
                break
        pass

    def viewRowInsert(self, view, source_model):
        view_model = view.model() 
        selection_model = view.selectionModel()
        row_indexes = selection_model.selectedRows()
        key_name = view_model.filterRegExp().pattern() 

        # 한줄만 선택 
        for row_index in row_indexes:
            source_index = None
            if( source_model == view_model ):
                source_index = row_index
            else :
                source_index = view_model.mapToSource( row_index ) 
            insert_row = source_index.row() 

            row_items = [''] * view_model.columnCount()
            row_items[0] = key_name
            self.insertRowToModel(source_model, row_items, insert_row)
            break
        pass

    def viewRowDelete(self, view):
        view_model = view.model()
        selection_model = view.selectionModel()
        row_indexes = selection_model.selectedRows()

        # 한줄만 선택 
        for row_index in row_indexes:
            view_model.removeRow(row_index.row())
            break
        pass
        
    @pyqtSlot()
    def onParameterViewCopyed(self):
        self.viewRowCopy(self.viewParameter)
    @pyqtSlot()
    def onParameterViewPasted(self):
        self.viewRowPaste(self.viewParameter, self.model_parameters)
    @pyqtSlot()
    def onParameterViewInserted(self):
        self.viewRowInsert(self.viewParameter, self.model_parameters)
    @pyqtSlot()
    def onParameterViewDeleted(self):
        self.viewRowDelete( self.viewParameter)


    @pyqtSlot()
    def onGroupViewCopyed(self):
        self.viewRowCopy(self.viewGroup)
    @pyqtSlot()
    def onGroupViewPasted(self):
        self.viewRowPaste(self.viewGroup, self.model_group)
    @pyqtSlot()
    def onGroupViewInserted(self):
        self.viewRowInsert(self.viewGroup, self.model_group)
    @pyqtSlot()
    def onGroupViewDeleted(self):
        self.viewRowDelete( self.viewGroup)
            
    @pyqtSlot()
    def onMsgInfoViewCopyed(self):
        self.viewRowCopy(self.viewMsgInfo)
    @pyqtSlot()
    def onMsgInfoViewPasted(self):
        self.viewRowPaste(self.viewMsgInfo, self.model_msg_info)
    @pyqtSlot()
    def onMsgInfoViewInserted(self):
        self.viewRowInsert(self.viewMsgInfo, self.model_msg_info)
    @pyqtSlot()
    def onMsgInfoViewDeleted(self):
        self.viewRowDelete( self.viewMsgInfo)


    @pyqtSlot()
    def onMsgValueViewCopyed(self):
        self.viewRowCopy(self.viewMsgValue)
    @pyqtSlot()
    def onMsgValueViewPasted(self):
        self.viewRowPaste(self.viewMsgValue, self.model_msg_values)
    @pyqtSlot()
    def onMsgValueViewInserted(self):
        self.viewRowInsert(self.viewMsgValue, self.model_msg_values)
    @pyqtSlot()
    def onMsgValueViewDeleted(self):
        self.viewRowDelete( self.viewMsgValue)

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())