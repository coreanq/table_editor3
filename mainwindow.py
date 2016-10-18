import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp, Qt, QItemSelectionModel
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
        self.model_group_info = QStandardItemModel(self)
        self.model_parameters = QStandardItemModel(self)
        self.model_proxy_parameters = QSortFilterProxyModel(self)
        
        self.model_msg = QStandardItemModel(self)
        self.model_msg_values = QStandardItemModel(self)
        self.model_proxy_msg_values = QSortFilterProxyModel(self)
        
        self.model_vari = QStandardItemModel(self)
        self.model_proxy_vari = QSortFilterProxyModel(self)
        
        self.model_title = QStandardItemModel()
        self.model_proxy_title = QSortFilterProxyModel(self)
        
        self.initView()
        self.createConnection()
        pass

    def createConnection(self):
        self.viewGroup.clicked.connect(self.onViewGroupClicked)  
        self.viewMessage.clicked.connect(self.onViewMessageClicked)
        
        parameter_view_eater = ve.ParameterViewKeyEater(self)
        self.viewParameter.installEventFilter(parameter_view_eater)
        parameter_view_eater.sig_copy_clicked.connect(self.parameterViewCopyed)
        parameter_view_eater.sig_paste_clicked.connect(self.parameterViewPasted)
        parameter_view_eater.sig_insert_clicked.connect(self.parameterViewInserted)
        parameter_view_eater.sig_delete_clicked.connect(self.parameterViewDeleted)
        
        pass
    def initView(self):
        view_list = [self.viewGroup, self.viewGroupInfo, 
                    self.viewParameter, self.viewMessage, 
                    self.viewMessageValue, self.viewVariable, 
                    self.viewTitle]
        
        self.viewGroup.setModel(self.model_group)
        self.viewGroupInfo.setModel(self.model_group_info)
        self.model_parameters.setHorizontalHeaderLabels(ci.para_col_info_for_view() )
        self.model_proxy_parameters.setSourceModel(self.model_parameters)
        self.viewParameter.setModel(self.model_proxy_parameters) 
       
        self.viewMessage.setModel(self.model_msg)
        self.viewMessageValue.setModel(self.model_proxy_msg_values)
        self.model_proxy_msg_values.setSourceModel(self.model_msg_values)
        
        self.viewVariable.setModel(self.model_proxy_vari)
        self.model_proxy_vari.setSourceModel(self.model_vari)
        
        self.viewTitle.setModel(self.model_proxy_title)
        self.model_proxy_title.setSourceModel(self.model_title)

        # 모든 view 기본 설정  
        for item in view_list:
            item.setAlternatingRowColors(True)
            item.setSelectionBehavior(QAbstractItemView.SelectRows)
            item.setDragEnabled(True)
            item.setDragDropMode(QAbstractItemView.InternalMove)
            item.setDefaultDropAction(Qt.MoveAction)
            item.setSelectionMode(QAbstractItemView.SingleSelection)
            headerView = item.horizontalHeader()
            # headerView.setStretchLastSection(True)
            headerView.setSectionResizeMode(QHeaderView.ResizeToContents)
            
        self.initDelegate()
            
    def initDelegate(self):
        cmb_title_delegate = cbd.ComboboxDelegate()
        cmb_title_delegate.setEditable( False ) 
        self.viewParameter.setItemDelegateForColumn(ci.para_col_info_for_view().index('Code TITLE'), cmb_title_delegate)
    pass
        
    @pyqtSlot(QModelIndex)
    def onViewGroupClicked(self, index):
        # print(util.whoami() )
        row = index.row()
        grp_name = self.model_group.item(row, 0 ).text() 
        grp_name = grp_name.split('_')[1]
        regx = QRegExp(grp_name.strip()) 
        self.model_proxy_parameters.setFilterKeyColumn(0)
        self.model_proxy_parameters.setFilterRegExp(regx)
        # 클립 보드 삭제 
        clipboard = QApplication.clipboard()
        clipboard.clear()
        pass
     
    @pyqtSlot(QModelIndex)
    def onViewMessageClicked(self, index):
        # print(util.whoami() )
        row = index.row()
        msg_name = self.model_msg.item(row, 0).text()
        regx = QRegExp(msg_name.strip() )
        self.model_proxy_msg_values.setFilterKeyColumn(0)
        self.model_proxy_msg_values.setFilterRegExp(regx)
         
        pass
    def searchTitlefromEnumName(self, enumName):
        items = self.model_title.findItems(enumName, column = ci.title_col_info().index('Enum 이름'))
        for item in items:
            return item.text()
        return ("Error")
        pass

    def readDataFromFile(self):
        TARGET_DIR = r'D:\download\1'
        for root, directories, filenames in os.walk(TARGET_DIR):
            # print(root, directories, filenames)
            for filename in filenames:
                if( filename.lower() in rd.parsing_files):
                    contents = ""
                    filePath = root + os.sep + filename
                    with open(filePath, 'r', encoding='utf8') as f:
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
                                                items[col_info.index('Msg')],
                                                items[col_info.index('Unit')],
                                                comm_write_protect,
                                                read_only, 
                                                no_modify_on_run,
                                                is_insert_zero_possible,
                                                items[col_info.index('ShowVari')],
                                                items[col_info.index('ShowVal')],
                                                '', # TODO eep주소 
                                                '', # TODO 통신주소 
                                                items[col_info.index('MaxEDS')],
                                                items[col_info.index('MinEDS')],
                                                items[col_info.index('Comment')]
                                ]
                                self.addRowToModel(self.model_parameters, view_col_list)
                            except IndexError:
                                print('error occur')
                                print(items)
                            
                        for item in rd.read_grp_info(contents):
                            self.addRowToModel(self.model_group, item)
                            pass
                        pass
                    elif( filename.lower() == rd.KPD_PARA_MSG_SRC_FILE):
                        msg_list = [] 
                        for item in rd.read_para_msg(contents):
                            msg_info = [item[0], item[1], item[2]]
                            if( msg_info not in msg_list ):
                                msg_list.append(msg_info) 
                            self.addRowToModel(self.model_msg_values, item)
                            pass
                        for msg_info in msg_list:
                            self.addRowToModel(self.model_msg, msg_info)
                            
                    elif( filename.lower() == rd.KPD_PARA_VARI_HEADER_FILE):
                        for item in rd.read_kpd_para_vari(contents):
                            self.addRowToModel(self.model_vari, item)
                        pass
                    elif ( filename.lower() == rd.KPD_BASIC_TITLE_SRC_FILE):
                        for item in rd.read_basic_title(contents):
                            # 항상 add title 보다 앞서야 하므로 
                            self.addRowToModel(self.model_title, item, editing = False)

                    elif ( filename.lower() == rd.KPD_ADD_TITLE_SRC_FILE ):
                        for item in rd.read_add_title(contents):
                            self.addRowToModel(self.model_title, item)
                    pass
        pass
        
    def addRowToModel(self, model, datas, editing = True):
        item_list = []
        for data in datas:
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
        
    @pyqtSlot()
    def parameterViewCopyed(self):
        clipboard = QApplication.clipboard()
        model = self.model_parameters
        filter_model = self.model_proxy_parameters
        s_model = self.viewParameter.selectionModel()
        row_indexes = []
        if(s_model.hasSelection() ):
            row_indexes = s_model.selectedRows()
        # 한개만 선택됨  
        for row_index in row_indexes:
            source_index = filter_model.mapToSource( row_index )
            row_data =  ','.join(model.item( source_index.row() , i).text() for i in range(model.columnCount() ) )
            print(row_data)
            clipboard.setText(row_data)
        pass
        
    @pyqtSlot()
    def parameterViewPasted(self):
        clipboard = QApplication.clipboard()
        model = self.model_parameters
        filter_model = self.model_proxy_parameters
        s_model = self.viewParameter.selectionModel()
        row_indexes = []
        
        insert_index = 0  
        if(s_model.hasSelection() ):
            row_indexes = s_model.selectedRows()
            # 한개만 선택됨 
            for row_index in row_indexes:
                source_index = filter_model.mapToSource( row_index )
                insert_index = source_index.row() 
        else:
            insert_index = model.rowCount()
        datas = clipboard.text().split(',')
        self.insertRowToModel(model, datas, insert_index)
        print(datas)
        pass 
        
    @pyqtSlot()
    def parameterViewInserted(self):
        model = self.model_parameters
        filter_model = self.model_proxy_parameters
        s_model = self.viewParameter.selectionModel()
        row_indexes = []
        
        insert_index = 0  
        if(s_model.hasSelection() ):
            row_indexes = s_model.selectedRows()
            # 한개만 선택됨 
            for row_index in row_indexes:
                source_index = filter_model.mapToSource( row_index )
                insert_index = source_index.row() 
        else:
            insert_index = model.rowCount()
        grp_name = filter_model.filterRegExp().pattern() 
        row_items = []
        for i in range(model.columnCount() ) :
            item = ''
            if( i == 0 ):
                item = grp_name
            row_items.append(item)
        
        self.insertRowToModel(model, row_items, insert_index)
        pass

    def parameterViewDeleted(self):
        model = self.model_parameters
        filter_model = self.model_proxy_parameters
        s_model = self.viewParameter.selectionModel()
        row_indexes = []
        
        delete_index = 0  
        if(s_model.hasSelection() ):
            row_indexes = s_model.selectedRows()
            # 한개만 선택됨 
            for row_index in row_indexes:
                source_index = filter_model.mapToSource( row_index )
                delete_index = source_index.row() 
            model.removeRow(delete_index)
        else:
            pass
            
    def groupViewCopyed(self):
        pass


if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = MainWindow()
    form.readDataFromFile()
    form.show()
    sys.exit(app.exec_())