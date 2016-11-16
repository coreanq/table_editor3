import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView,  \
                            QAction, QFileDialog
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, \
                         QRegExp, Qt, QItemSelectionModel, QStringListModel, \
                         QIODevice, QFile
import json
import mainwindow_ui 
import view_delegate as cbd 
import view_key_eater as ve
import column_info as ci
import read_data as rd
import resource_rc as rsc
import util
import re

ATTR_BYTE = 0x0001  # byte 단위 사용 안함 
ATTR_UP = 0x0002
ATTR_LP = 0x0004
ATTR_READ_ONLY = 0x0008
ATTR_NO_CHANGE_ON_RUN =  0x0010
ATTR_ZERO_INPUT = 0x0020
ATTR_NO_COMM =0x0040
ATTR_ENT = 0x0080
ATTR_HIDDEN_CON = 0x0700
ATTR_ADD  = 0x1000

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
        
        self.model_var = QStandardItemModel(self)
        self.model_proxy_var = QSortFilterProxyModel(self)
        
        self.model_title = QStandardItemModel()
        self.model_proxy_title = QSortFilterProxyModel(self)

        #delegate 선언 
        self.delegate_parameters_view = cbd.ViewDelegate(self)
        self.delegate_msg_view = cbd.ViewDelegate(self)
        self.delegate_group_view = cbd.ViewDelegate(self)
        
        self.model_kpd_para_unit = QStandardItemModel()

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

        msg_value_view_eater = ve.ViewKeyEater(self)
        self.viewTitle.installEventFilter(msg_value_view_eater)
        msg_value_view_eater.sig_copy_clicked.connect(self.onTitleViewCopyed)
        msg_value_view_eater.sig_paste_clicked.connect(self.onTitleViewPasted)
        msg_value_view_eater.sig_insert_clicked.connect(self.onTitleViewInserted)
        msg_value_view_eater.sig_delete_clicked.connect(self.onTitleViewDeleted)

        msg_value_view_eater = ve.ViewKeyEater(self)
        self.viewVariable.installEventFilter(msg_value_view_eater)
        msg_value_view_eater.sig_copy_clicked.connect(self.onVariableViewCopyed)
        msg_value_view_eater.sig_paste_clicked.connect(self.onVariableViewPasted)
        msg_value_view_eater.sig_insert_clicked.connect(self.onVariableViewInserted)
        msg_value_view_eater.sig_delete_clicked.connect(self.onVariableViewDeleted)

        # parametere view  더블 클릭시 unit의 msg combobox 내용을 변경하기 위함  
        self.viewParameter.doubleClicked.connect(self.onViewParameterDoubleClicked)
        self.model_parameters.dataChanged.connect(self.onModelParameterDataChanged)

        self.menuFile.triggered[QAction].connect(self.onMenuFileActionTriggered)
        self.menuEdit.triggered[QAction].connect(self.onMenuEditActionTriggered)
        self.menuAbout.triggered[QAction].connect(self.onMenuAboutActionTriggered)


    @pyqtSlot(QAction)
    def onMenuFileActionTriggered(self, action):
        print(action.text())
        action_type = action.text()

        current_path = os.getcwd()
        if( action_type == 'Open'):
            selected_dir = QFileDialog.getExistingDirectory(
                                            self, 
                                            caption = 'Open', 
                                            directory = current_path, 
                                            options = QFileDialog.ShowDirsOnly
                                            )
            
            if( os.path.isdir(selected_dir) ):
                if( self.readDataFromFile(selected_dir) ):
                    self.lineSourcePath.setText(selected_dir)
            pass
        elif( action_type == 'Save'):
            pass
        elif( action_type =='Save As'):
            pass
        elif( action_type == 'Exit'):
            pass
       

    @pyqtSlot(QAction)
    def onMenuEditActionTriggered(self, action):
        print(action.text())

    @pyqtSlot(QAction)
    def onMenuAboutActionTriggered(self, action):
        print(action.text())

    def initView(self):
        view_list = [self.viewGroup,  
                    self.viewParameter, self.viewMsgInfo, 
                    self.viewMsgValue, self.viewVariable, 
                    self.viewTitle]

        # group view init 
        col_info = ci.group_col_info()
        view = self.viewGroup
        self.model_proxy_group.setSourceModel(self.model_group)
        self.model_group.setHorizontalHeaderLabels(col_info)
        view.setModel(self.model_proxy_group)
        view.setColumnHidden(col_info.index('Dummy Key'), True)

        # prameter view init
        col_info = ci.para_col_info_for_view()
        view = self.viewParameter
        self.model_proxy_parameters.setSourceModel(self.model_parameters)
        self.model_parameters.setHorizontalHeaderLabels(col_info)
        view.setModel(self.model_proxy_parameters) 
        view.setColumnHidden( col_info.index('Group'), True)
       
        # msg info view init 
        col_info = ci.msg_info_col_info()
        view = self.viewMsgInfo
        self.model_proxy_msg_info.setSourceModel(self.model_msg_info) 
        self.model_msg_info.setHorizontalHeaderLabels(col_info )
        view.setModel(self.model_proxy_msg_info)
        view.setColumnHidden( col_info.index('Dummy Key'), True)

        # msg value view init 
        col_info = ci.msg_values_col_info()
        view = self.viewMsgValue
        self.model_proxy_msg_values.setSourceModel(self.model_msg_values)
        self.model_msg_values.setHorizontalHeaderLabels(col_info)
        view.setModel(self.model_proxy_msg_values)
        view.setColumnHidden(col_info.index('MsgName'), True)
        view.setColumnHidden(col_info.index('MsgInfo'), True)
        
        # var view init
        col_info = ci.variable_col_info()
        view = self.viewVariable
        self.model_proxy_var.setSourceModel(self.model_var)
        self.model_var.setHorizontalHeaderLabels(col_info)
        view.setModel(self.model_proxy_var)
        view.setColumnHidden(col_info.index('Dummy Key'), True)

        # title view init 
        col_info = ci.title_col_info()
        view = self.viewTitle
        self.model_proxy_title.setSourceModel(self.model_title)
        self.model_title.setHorizontalHeaderLabels(col_info)
        view.setModel(self.model_proxy_title)
        view.setColumnHidden(col_info.index('Dummy Key'), True)

        # filter 값을 이상한 값으로 넣어 처음에는 아무 리스트가 안나타나게 함 
        proxy_list = [  self.model_proxy_msg_values, self.model_proxy_parameters, 
                        # self.model_proxy_title, self.model_proxy_var  
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

    def setCmbDelegateAttribute(self, model, view, delegate, columns = [], editable = False, 
        width = 0, cmb_model_column = 0):
        for col_index in columns:
            delegate.setEditable(col_index,  editable ) 
            delegate.setEditorType(col_index, 'combobox')
            delegate.setModel(col_index, model)
            delegate.setModelColumn(col_index, cmb_model_column)
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
        cmb_model_column_index = ci.title_col_info().index('Title')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], width = 150, 
                cmb_model_column = cmb_model_column_index )

        model = self.model_kpd_para_unit
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_index = col_info.index('단위')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], editable = False,  width = 150)

        model = self.model_var
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ col_info.index('Para 변수'), 
                        col_info.index('최대값'),
                        col_info.index('최소값'),
                        col_info.index('보임변수')
        ]
        cmb_model_column_index = ci.variable_col_info().index('Variable')
        self.setCmbDelegateAttribute(model, view, delegate, col_indexes, editable = True,  
                width = 150, cmb_model_column = cmb_model_column_index)

        model = QStringListModel( ['True', 'False']) 
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ col_info.index('통신쓰기금지'), 
                        col_info.index('읽기전용'),
                        col_info.index('운전중변경불가'),
                        col_info.index('0 입력가능')
        ]
        self.setCmbDelegateAttribute(model, view, delegate, col_indexes )

        model = QStringListModel( ['AfterEnter', 'Cmd']) 
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ col_info.index('KPD 타입') ]
        self.setCmbDelegateAttribute(model, view, delegate, col_indexes, width = 80)

        # msg view delegate 설정 
        model = self.model_title
        view  = self.viewMsgValue
        delegate = self.delegate_msg_view  
        col_info = ci.msg_values_col_info()
        col_index = col_info.index('Title')
        cmb_model_column_index = ci.title_col_info().index('Title')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], width = 150, 
                cmb_model_column = cmb_model_column_index)

        # group view delegate 설정 
        model = self.model_var
        view  = self.viewGroup
        delegate = self.delegate_group_view  
        col_info = ci.group_col_info()
        col_index = col_info.index('Hidden Var')
        cmb_model_column_index = ci.variable_col_info().index('Variable')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], editable = True , 
                width = 150, cmb_model_column = cmb_model_column_index  )
        pass
       
    # unit 선택에 따라서 수시로 변하기 때문에 따로 함수로 만들어 줌 
    def onParameterViewUnitChanged(self, index): 
        col_info = ci.para_col_info_for_view()
        model = self.model_parameters
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        delegate_model = None

        unit_col = col_info.index('단위')
        form_msg_col = col_info.index('폼메시지')

        unit_data = model.item(index.row() , unit_col).text()
        cmb_model_col  = 0 

        if( unit_data == 'U_DATAMSG' or unit_data == 'U_RPM_CHG_DATAMSG'):
            # 생성되는 cmb box 의 모델의 참조 column index 를 정해줌 
            delegate_model = self.model_msg_info
            cmb_model_col = ci.msg_info_col_info().index('MsgName')
        elif( unit_data == 'U_HZ_RPM'):
            delegate_model = ci.unit_with_msg()[unit_data]
        elif( unit_data == 'U_B'):
            delegate_model = ci.unit_with_msg()[unit_data]
        else: 
            delegate_model = ci.unit_with_msg()['Other']
        self.setCmbDelegateAttribute(delegate_model, view, delegate, [form_msg_col], 
                editable = False,  width = 150, cmb_model_column = cmb_model_col)

        pass 

    # 통신 쓰기 금지 선택에 따라서 통신 주소가 수시로 변하기 때문에 따로 함수로 만들어 줌 
    def onParameterViewNoCommChanged(self, index): 
        col_info = ci.para_col_info_for_view()
        model = self.model_parameters
        row = index.row()

        no_comm_col = col_info.index('통신쓰기금지')
        comm_addr_col = col_info.index('통신주소')

        no_comm_data = model.item(row , no_comm_col).text()

        # 통신 주소 설정 
        group_name = model.item(row, col_info.index('Group')).text()
        code_num = int(model.item(row, col_info.index('Code#')).text())
        
        find_items= self.model_group.findItems(group_name, column = ci.group_col_info().index('Group'))
        group_num = 0 

        for find_item in find_items:
            group_num =  find_item.row()
        
        if( no_comm_data == 'True'):
            comm_addr = '통신 쓰기 금지'
        else:
            comm_addr = self.makeAddrValue(group_num, code_num)

        model.setItem(index.row(), comm_addr_col, QStandardItem(comm_addr))
        pass

    @pyqtSlot(QModelIndex)
    def onViewGroupClicked(self, index):
        # print(util.whoami() )
        row = index.row()
        col_info = ci.group_col_info()
        key_name = self.model_group.item(row, col_info.index('Group')).text() 
        regx = QRegExp(key_name.strip()) 
        self.model_proxy_parameters.setFilterKeyColumn(0)
        self.model_proxy_parameters.setFilterRegExp(regx)
        pass
     
    @pyqtSlot(QModelIndex)
    def onViewMsgInfoClicked(self, index):
        # print(util.whoami() )
        row = index.row()
        col_info = ci.msg_info_col_info()
        key_name = self.model_msg_info.item(row, col_info.index('MsgName')).text()
        regx = QRegExp(key_name.strip() )
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

    def makeAddrValue(self, group_num, code_num ):
        comm_addr = hex(0x1000 + (0x0100 * group_num) + code_num)
        comm_addr = '0x{0}'.format( comm_addr[2:].upper() )
        return comm_addr

    def makeEEPAddrValue(self, group_num, code_num ):
        eep_addr = hex(0x0200 + (16 * 2 * 7 * group_num) + (code_num * 2 + 16) )
        eep_addr = '0x{0}'.format( eep_addr[2:].upper() )
        return eep_addr
    def makeHiddenCondition(self, attribute):
        hidden_condition = '' 
        val = (attribute & ATTR_HIDDEN_CON) >> 8
        if( val == 0 ):
            hidden_condition = '=='
        elif ( val == 1 ):
            hidden_condition = '>'
        elif ( val == 2 ):
            hidden_condition = '<'
        elif( val  == 3 ) :
            hidden_condition = '!='
        return hidden_condition
    
    def hiddenConditionToValue(self, hidden_condition ):
        value = 0
        if( hidden_condition == '=='):
            value = 0
        elif ( hidden_condition == '>'):
            value = 1
        elif( hidden_condition == '<'):
            value = 2
        elif( hidden_condition == '!='):
            value = 3
        return value

    # read_para_table 에서는 단순히 파일을 파싱해서 올려주는 역할만 하고 
    # 올라온 데이터에 대한 수정은 상위단에서 수행하도록 함 
    def readDataFromFile(self, source_path):
        target_dir = source_path
        source_file_list = []
        # 파싱에 필요한 모든 파일이 다 존재 하는지 확인 
        for (dirpath, dirnames, filenames) in os.walk(target_dir):
            source_file_list = filenames
            # root folder 만 확인할것이므로 바로 break 
            break
        source_file_list = [ file.lower() for file in source_file_list ]

        if( all ( x in source_file_list for x in rd.parsing_files) == False):
            print(source_file_list)
            return False

        for filename in rd.parsing_files:
            file_path = target_dir + os.sep + filename 
            if( os.path.exists(file_path) ):
                contents = ""
                with open(file_path, 'r', encoding='utf8') as f:
                    contents = f.read()
                if(filename.lower() == rd.KPD_PARA_TABLE_SRC_FILE ):
                    # 그룹  정보 읽기 
                    for items in rd.read_grp_info(contents):
                        self.addRowToModel(self.model_group, items)
                        pass

                    for items in rd.read_para_table(contents):
                        col_info = ci.para_col_info_for_file()
                        arg = items[col_info.index('Attribute')] 
                        attribute  = int(arg, 16)

                        no_comm, read_only, no_change_on_run, zero_input = False, False, False, False
                        key_pad_type = 'Cmd'
                        hidden_condition = ''

                        if( attribute & ATTR_NO_COMM ):
                            no_comm = True 
                        if( attribute & ATTR_READ_ONLY ):
                            read_only = True
                        if( attribute & ATTR_NO_CHANGE_ON_RUN ):
                            no_change_on_run = True 
                        if( attribute & ATTR_ZERO_INPUT ):
                            zero_input = True 
                        if( attribute & ATTR_ENT):
                            key_pad_type = 'AfterEnter'
                        hidden_condition = self.makeHiddenCondition(attribute)

                        # 통신 주소 설정 
                        group_name = items[col_info.index('Group')]
                        code_num = int(items[col_info.index('Code#')])
                        
                        find_items= self.model_group.findItems(group_name, column = ci.group_col_info().index('Group'))
                        group_num = 0 

                        for find_item in find_items:
                            group_num  =  find_item.row()
                        
                        if( no_comm ):
                            comm_addr = '통신 쓰기 금지'
                        else:
                            comm_addr = self.makeAddrValue(group_num, code_num)
                        eep_addr = self.makeEEPAddrValue(group_num, code_num)
                            
                        title = self.searchTitlefromEnumName(items[col_info.index('TitleIndex')])
                        try : 
                            view_col_list = [ items[col_info.index('Group')],  
                                            items[col_info.index('Code#')],  
                                            title, 
                                            items[col_info.index('AtValue')], 
                                            items[col_info.index('ParaVar')],
                                            items[col_info.index('KpdFunc')],
                                            items[col_info.index('DefaultVal')],
                                            items[col_info.index('MaxVal')],
                                            items[col_info.index('MinVal')],
                                            items[col_info.index('Msg')].replace('MSG_', ''),
                                            items[col_info.index('Unit')],
                                            hidden_condition,
                                            key_pad_type,
                                            str(no_comm),
                                            str(read_only), 
                                            str(no_change_on_run),
                                            str(zero_input),
                                            items[col_info.index('ShowVar')],
                                            items[col_info.index('ShowVal')],
                                            eep_addr,
                                            comm_addr, 
                                            items[col_info.index('MaxEDS')],
                                            items[col_info.index('MinEDS')],
                                            items[col_info.index('Comment')]
                            ]
                            self.addRowToModel(self.model_parameters, view_col_list)
                        except IndexError:
                            print('error occur')
                            print(items)
                        
                elif( filename.lower() == rd.KPD_PARA_MSG_SRC_FILE):
                    msg_list = [] 
                    col_info = ci.msg_values_col_info()
                    title_index = col_info.index('Title')
                    for items in rd.read_para_msg(contents):
                        msg_info = ['', items[col_info.index('MsgName')], items[col_info.index('MsgInfo')]] 

                        if( msg_info not in msg_list ):
                            msg_list.append(msg_info) 
                        title = self.searchTitlefromEnumName(items[title_index])
                        insert_list = *items[:title_index], title,  *items[title_index +1: ]
                        self.addRowToModel(self.model_msg_values, insert_list)
                        pass

                    for item in msg_list:
                        self.addRowToModel(self.model_msg_info, item)
                        
                elif( filename.lower() == rd.KPD_PARA_VAR_HEADER_FILE):
                    for items in rd.read_kpd_para_var(contents):
                        self.addRowToModel(self.model_var, items)
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
        return True
        pass
        
    def addRowToModel(self, model, data_list, editing = True):
        item_list = []
        for data in data_list:
            item = QStandardItem(data)
            if( not editing ):
                item.setBackground(QColor(Qt.lightGray) )
                item.setFlags(Qt.NoItemFlags)
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
    def onViewParameterDoubleClicked(self, index):
        # view 에서 발생한 것은 proxy_index 
        # unit 과 메시지를 클릭했을때 delegate 를 설정해줘야 함 
        proxy_model = self.model_proxy_parameters
        source_index = proxy_model.mapToSource(index) 

        unit_col = ci.para_col_info_for_view().index('단위')
        form_msg_col = ci.para_col_info_for_view().index('폼메시지')
        if( index.column() == unit_col or index.column() == form_msg_col ):
           self.onParameterViewUnitChanged( self.model_parameters.index(source_index.row(), unit_col )  ) 
        pass

    @pyqtSlot(QModelIndex, QModelIndex)
    def onModelParameterDataChanged(self, topLeft, bottomRight):
        topx = topLeft.row()
        topy = topLeft.column() 

        bottomx = bottomRight.row()
        bottomy = bottomRight.column()

        unit_col = ci.para_col_info_for_view().index('단위')
        no_comm_col = ci.para_col_info_for_view().index('통신쓰기금지') 

        if( unit_col  in range(topy, bottomy + 1) ):
            for row in range(topx, bottomx + 1):
                self.onParameterViewUnitChanged( self.model_parameters.index(row, unit_col )  )
            pass
        if( no_comm_col in range(topy, bottomy + 1)):
            for row in range(topx, bottomx + 1):
                self.onParameterViewNoCommChanged( self.model_parameters.index(row, no_comm_col) )
            pass

        pass 

    def viewRowCopy(self, subject, view):
        clipboard = QApplication.clipboard()
        view_model = view.model()
        selection_model = view.selectionModel()
        row_indexes = selection_model.selectedRows()
        data_dict = {}

        # ' "subject" : [ 'item1, item2...', 'item1, item2...' ] '
        for row_index in row_indexes:
            row_data = ','.join(view_model.data(row_index.sibling(row_index.row(), column)) for column in range(view_model.columnCount() )) 
            previous_data = data_dict.get(subject,[])
            previous_data.append(row_data)
            data_dict[subject] = previous_data
        # print(json.dumps(data_dict, indent= 4 ))
        clipboard.setText(json.dumps(data_dict))
        # print('\n'.join(rows))
        pass

    def viewRowPaste(self, subject, view, source_model):
        clipboard = QApplication.clipboard()
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
            dict_result = json.loads(clipboard.text())

            for key, lists in dict_result.items():
                if( key == subject ):
                    for row in lists:
                        row_items = row.split(',')
                        row_items[0] = key_name
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
        self.viewRowCopy('parameter', self.viewParameter )
    @pyqtSlot()
    def onParameterViewPasted(self):
        self.viewRowPaste('parameter', self.viewParameter, self.model_parameters)
    @pyqtSlot()
    def onParameterViewInserted(self):
        self.viewRowInsert(self.viewParameter, self.model_parameters)
    @pyqtSlot()
    def onParameterViewDeleted(self):
        self.viewRowDelete( self.viewParameter)

    @pyqtSlot()
    def onGroupViewCopyed(self):
        self.viewRowCopy('group', self.viewGroup)
    @pyqtSlot()
    def onGroupViewPasted(self):
        self.viewRowPaste('group', self.viewGroup, self.model_group)
    @pyqtSlot()
    def onGroupViewInserted(self):
        self.viewRowInsert(self.viewGroup, self.model_group)
    @pyqtSlot()
    def onGroupViewDeleted(self):
        self.viewRowDelete( self.viewGroup)
            
    @pyqtSlot()
    def onMsgInfoViewCopyed(self):
        self.viewRowCopy('msg_info', self.viewMsgInfo)
    @pyqtSlot()
    def onMsgInfoViewPasted(self):
        self.viewRowPaste('msg_info', self.viewMsgInfo, self.model_msg_info)
    @pyqtSlot()
    def onMsgInfoViewInserted(self):
        self.viewRowInsert(self.viewMsgInfo, self.model_msg_info)
    @pyqtSlot()
    def onMsgInfoViewDeleted(self):
        self.viewRowDelete( self.viewMsgInfo)

    @pyqtSlot()
    def onMsgValueViewCopyed(self):
        self.viewRowCopy('msg_value', self.viewMsgValue)
    @pyqtSlot()
    def onMsgValueViewPasted(self):
        self.viewRowPaste('msg_value', self.viewMsgValue, self.model_msg_values)
    @pyqtSlot()
    def onMsgValueViewInserted(self):
        self.viewRowInsert(self.viewMsgValue, self.model_msg_values)
    @pyqtSlot()
    def onMsgValueViewDeleted(self):
        self.viewRowDelete( self.viewMsgValue)

    @pyqtSlot()
    def onTitleViewCopyed(self):
        self.viewRowCopy('title', self.viewTitle)
        pass
    @pyqtSlot()
    def onTitleViewPasted(self):
        self.viewRowPaste('title', self.viewTitle, self.model_title)
        pass
    @pyqtSlot()
    def onTitleViewInserted(self):
        self.viewRowInsert(self.viewTitle, self.model_title)
        pass
    @pyqtSlot()
    def onTitleViewDeleted(self):
        self.viewRowDelete(self.viewTitle)
        pass

    @pyqtSlot()
    def onVariableViewCopyed(self):
        self.viewRowCopy('variable', self.viewVariable)
        pass 
    @pyqtSlot()
    def onVariableViewPasted(self):
        self.viewRowPaste('variable', self.viewVariable, self.model_var)
        pass
    @pyqtSlot()
    def onVariableViewInserted(self):
        self.viewRowInsert(self.viewVariable, self.model_var)
        pass
    @pyqtSlot()
    def onVariableViewDeleted(self):
        self.viewRowDelete(self.viewVariable)
        pass

    def make_add_title_eng(self):
        col_info = ci.title_col_info()
        model = self.model_title
        row = model.rowCount()
        col = model.columnCount()

        rows = []
        total_add_title = 0
        add_title_size = 0
        enum_list = []

        for row_index in range(row):
            row_items = []
            for col_index in range(col):
                item = model.item(row_index, col_index)
                row_items.append(item.text()) 

            title = row_items[col_info.index('Title')]
            enum_name = row_items[col_info.index('Enum 이름')]
            title_index = row_items[col_info.index('Title Index')]
            data = row_items[col_info.index('Data')]

            # enum_list 생성용  for kpd_title_enum.h
            if( int(title_index) == 1000):
                enum_list.append('T_TotalDefaultTitleSize')
                enum_list.append(r'{0:<32} = START_ADD_TITLE_INDEX//{1}'.format(enum_name, title_index))
            else:
                enum_list.append(r'{0:<32}//{1}'.format(enum_name, title_index))

            if( int(title_index) < 1000):
                continue

            total_add_title = total_add_title + 1   
            # hex data 4개씩 짜름 
            re_split = re.compile(r'[a-z0-9A-Z]{4,4}')
            find_list = re_split.findall(data)
            add_title_size = len(find_list)
            find_merge = ','.join('0x'+item for item in find_list )
            rows.append(r'{{{0}}}//{1:<5}"{2:<20}"{3}'.format(find_merge, title_index, title, enum_name))
        # print('\n'.join(rows))

        
        src_template= \
'''//================================================
//이 프로그램은 ADD Title용              
//================================================
#include "BaseDefine.H"
#include "AddTitle_Eng.H"\n\n\
const WORD g_awAddTitleEng[TOTAL_ADD_TITLE][ADD_TITLE_SIZE] = {{ \n 
 {0}
}};
'''
        file_contents = src_template.format('\n,'.join(rows))

        TARGET_DIR = r"d:\download\1\result"
        with open(TARGET_DIR + os.path.sep + 'addtitle_eng.c_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass

        header_template= \
'''#ifndef ADD_TITLE_ENG_H
#define ADD_TITLE_ENG_H\n\n
#define TOTAL_ADD_TITLE       {0} 
#define ADD_TITLE_SIZE        {1} 
extern const WORD g_awAddTitleEng[TOTAL_ADD_TITLE][ADD_TITLE_SIZE];\n
#endif   //ADD_TITLE_ENG_H 
'''

        file_contents = header_template.format(total_add_title, add_title_size)
        with open(TARGET_DIR + os.path.sep + 'addtitle_eng.h_temp', 'w') as f:
            f.write(file_contents)
        pass


        kpd_title_enum_header_template= \
'''#ifndef KPD_TITLE_ENUM_H
#define KPD_TITLE_ENUM_H
    
/***********************************************
   Keypad Title을 사용하기 위한 Enum정의        
***********************************************/
#define START_ADD_TITLE_INDEX 1000
    
enum{{ 
 {0}
}};
{1}
#endif
'''
        enum_list.append('T_TotalAddTitleSize')
        if( total_add_title ):
            have_add_title = '#define HAVE_ADD_TITLE	//Add Title이 존재할때만 Define 된다.'
        else:
            have_add_title = ''
        file_contents = kpd_title_enum_header_template.format('\n ,'.join(enum_list), have_add_title)
        with open(TARGET_DIR + os.path.sep + 'kpd_title_enum.h_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass

    def make_kpdpara_var(self):
        col_info = ci.variable_col_info()
        model = self.model_var
        row = model.rowCount()
        col = model.columnCount()

        define_list = []
        var_list = []
        var_type = ''

        for row_index in range(row):
            row_items = []
            for col_index in range(col):
                item = model.item(row_index, col_index)
                row_items.append(item.text()) 

            variable = row_items[col_info.index('Variable')]
            var_type = row_items[col_info.index('Type')]
            description = row_items[col_info.index('Description')]

            re_split = re.compile(r'(k_[a-z0-9A-Z]+)(\[([0-9_A-Z]+)\])?')
            find_list = re_split.findall(variable)
            for var_name, dummy, var_arr_cnt in find_list:
                if( len(var_arr_cnt) ):
                    define_list.append(r'#define {0:<32}{1}'.format(var_name.upper(), var_arr_cnt ))
                    variable = re.sub(r'\[([0-9]+)\]', '[' + var_name.upper() + ']', variable )
                var_list.append('{0:<62}//{1}'.format(variable, description))


        header_template= \
'''/***********************************************
// TABLE EDITOR 3 : 인버터 파라메터 변수 선언
***********************************************/\n\n
#ifndef KPD_PARA_VARI_H
#define KPD_PARA_VARI_H\n
{0}\n\n\n
extern {1}                          //{1} TYPE의 변수들
{2}
;    
\n\n\n
#endif    //KPD_PARA_VARI_H
'''

        file_contents = header_template.format('\n'.join(define_list), var_type, '\n,'.join(var_list)) 
        # print(var_list)
        # print(define_list)
        # print(file_contents)
        TARGET_DIR = r"d:\download\1\result"
        with open(TARGET_DIR + os.path.sep + 'KpdPara_Vari.h_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass


        source_template = \
'''
/***********************************************
// TABLE EDITOR 3 : 인버터 파라메터 변수 선언
***********************************************/
    
    
#include "BaseDefine.H"
#include "KpdPara_Vari.H"
{0}                          //{0} TYPE의 변수들 
{1}
;
'''
        file_contents = source_template.format(var_type, '\n,'.join(var_list)) 
        with open(TARGET_DIR + os.path.sep + 'KpdPara_Vari.c_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass


    def make_kpdpara_msg(self):
        col_info = ci.msg_values_col_info()
        key_col_info = ci.msg_info_col_info()
        key_model = self.model_msg_info
        model = self.model_msg_values

        key_row = key_model.rowCount()
        key_col = key_model.columnCount()

        msg_name_count_list  = []
        msg_vars = [] 
        lines = []
        msg_var_template = \
'''static const S_MSG_TYPE t_ast{0}[MSG_COUNT_{1}] = {{                        //MSG_{2:<20}//{3}
     {4}
}};
'''
        msg_name_count = 0 # 각 msg name 에 몇개의 인자가 있는지 나타냄 yesno msg 의 경우 2개 
        msg_name, msg_comment, title_name, at_value  = '', '', '', ''
        # key model 에서 key 값을 추출하여 key_value 모델에서 find 함 
        for row_index in range(key_row):
            key_msg_name = key_model.item(row_index, key_col_info.index('MsgName')).text() 

            find_items = model.findItems(key_msg_name, column = col_info.index('MsgName'))

            for find_item in find_items:
                find_row_index = find_item.row()

                msg_name = model.item(find_row_index, col_info.index('MsgName')).text()
                msg_comment = model.item(find_row_index, col_info.index('MsgInfo')).text()
                title_name = model.item(find_row_index, col_info.index('Title')).text()
                at_value = model.item(find_row_index, col_info.index('AtValue')).text()

                title_items = self.model_title.findItems(title_name, column = ci.title_col_info().index('Title'))
                for item in title_items:
                    enum_name = self.model_title.item(item.row(), ci.title_col_info().index('Enum 이름')).text()

                lines.append('{{{0:<20},{1:<5}}}                       //"{2}"'.format(enum_name, at_value, title_name))
                msg_name_count =msg_name_count + 1
            
            msg_vars.append(
                msg_var_template.format(msg_name,
                                        msg_name.upper(), 
                                        msg_name, 
                                        msg_comment, 
                                        '\n\t,'.join(lines))
            )
            lines.clear()
            msg_name_count_list.append([msg_name, msg_name_count])
            msg_name_count = 0 
            


        source_template = \
'''//========================================= 
// TABLE EDITOR 3 : 인버터 Message들 저장   
//=========================================/ 
          
          
#include "BaseDefine.H"
#include "KPD_Title_Enum.H"
#include "KpdPara_Msg.H"
\n\n
static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], WORD wMsgNum);
\n\n
{0}\n
static const S_MSG_TYPE * t_pastMsgDataTbl[MSG_TOTAL] = {{
\t {1}
}};
static const WORD t_awMsgDataSize[MSG_TOTAL] = {{
\t {2}
}};\n
static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], WORD wMsgNum)
{{
	return astMsgType[wMsgNum];
}}
S_MSG_TYPE KpdParaGetMsgData(WORD wMsgIdx, WORD wMsgNum)
{{
	return KpdParaGetMsg(t_pastMsgDataTbl[wMsgIdx], wMsgNum);
}}
WORD KpdParaGetMsgSize(WORD wMsgIdx)
{{
	return t_awMsgDataSize[wMsgIdx];
}}

'''
        msg_data_tbl_lines = []
        msg_data_size_lines = []
        msg_data_enum_lines = []
        msg_enum_count = 0

        for msg_name, msg_name_count in msg_name_count_list:
            msg_data_tbl_lines.append('t_ast{0}'.format(msg_name))
            msg_data_size_lines.append('MSG_COUNT_{0}'.format(msg_name.upper()))
            msg_data_enum_lines.append('MSG_{0:<36}//{1:0>3}'.format(msg_name, msg_enum_count))
            msg_enum_count = msg_enum_count + 1

        file_contents = source_template.format(  '\n'.join(msg_vars),
                                                 '\n\t,'.join(msg_data_tbl_lines),
                                                 '\n\t,'.join(msg_data_size_lines) )
        TARGET_DIR = r"d:\download\1\result"
        with open(TARGET_DIR + os.path.sep + 'KpdPara_Msg.c_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass

        header_template =  \
'''
//========================================= 
// TABLE EDITOR 3 : 인버터 Message들 저장   
//========================================= 
#ifndef KEYPAD_MESSAG_H
#define KEYPAD_MESSAG_H
      
#include "KpdPara_StructUnit.H"
      
enum{{  //MSG들의 Index 값
\t\t {0}
}};
\n
{1}
\n\n
S_MSG_TYPE KpdParaGetMsgData(WORD wMsgIdx, WORD wMsgNum);
WORD KpdParaGetMsgSize(WORD wMsgIdx);
#endif  //KEYPAD_MESSAG_H

'''
        # 한라인 추가 되므로  msg_total 
        msg_data_enum_lines.append('MSG_{0:<36}//{1:0>3}'.format('TOTAL', msg_enum_count))
        msg_define_lines = []
        for msg_name, msg_name_count in msg_name_count_list:
            msg_define_lines.append('#define MSG_COUNT_{0:<30}{1}'.format(msg_name.upper(), msg_name_count))

        file_contents = header_template.format(  '\n\t\t,'.join(msg_data_enum_lines),
                                                 '\n'.join(msg_define_lines) )
        TARGET_DIR = r"d:\download\1\result"
        with open(TARGET_DIR + os.path.sep + 'KpdPara_Msg.h_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass

    def make_kpdpara_table(self):
        col_info = ci.para_col_info_for_view()
        model = self.model_parameters
        key_col_info = ci.group_col_info()
        key_model = self.model_group

        key_row = key_model.rowCount()

        # 소스용 variable template
        para_vars = [] 
        para_vars_lines = []
        para_vars_template = \
'''static const S_TABLE_X_TYPE t_ast{0}grp[GRP_{1}_CODE_TOTAL] = {{
{2}
}};
'''
        # 소스내 group info 용 template 
        group_info_lines  = []
        group_info_template ='{{T_{0:<10},{1:<20},{2:<25},{3:<10}}}'

        table_addr_lines = [] 
        table_addr_template = \
'''\tcase GROUP_{0}:
\t\tpstTable = &t_ast{0}grp[wTableIdx];
\t\tbreak;
'''

        # 헤더용 define template
        defines_lines = []
        defines_template = '#define GRP_{0}_CODE_TOTAL\t{1}'

        # group index 용 
        group_index_lines = []

        # key model 에서 key 값을 추출하여 key_value 모델에서 find 함 
        for row_index in range(key_row):
            # 그룹 정보 추출 
            key_group_name = key_model.item(row_index, key_col_info.index('Group')).text() 
            key_group_hidden_var = key_model.item(row_index, key_col_info.index('Hidden Var')).text()
            key_group_hidden_val = key_model.item(row_index, key_col_info.index('Hidden Val')).text()
            if( 'g_' in key_group_hidden_var or 'k_' in key_group_hidden_val ):
                key_group_hidden_var = '(WORD*)&' + key_group_hidden_var

            group_info_lines.append( 
                group_info_template.format(
                    key_group_name.upper(), 'GRP_' + key_group_name.upper() + '_CODE_TOTAL', 
                    key_group_hidden_var, key_group_hidden_val
                )
            )

            table_addr_lines.append( 
                table_addr_template.format(
                    key_group_name.upper()
                )
            )

            # 해당 하는 그룹의 아이템 정보를 얻음 
            find_items = model.findItems(key_group_name, column = col_info.index('Group'))
            per_group_item_count = len(find_items)

            defines_lines.append( 
                defines_template.format(
                    key_group_name.upper(),
                    per_group_item_count
                )
            )

            group_index_lines.append( 
                'GROUP_{0}'.format( key_group_name.upper() )
            )

            for find_item in find_items:
                find_row_index = find_item.row()

                group_name = model.item(find_row_index, col_info.index('Group')).text()
                code_num = model.item(find_row_index, col_info.index('Code#')).text()
                title_name = model.item(find_row_index, col_info.index('Code TITLE')).text()
                title_enum_name = ''
                title_items = self.model_title.findItems(title_name, column = ci.title_col_info().index('Title'))
                for item in title_items:
                    title_enum_name = self.model_title.item(item.row(), ci.title_col_info().index('Enum 이름')).text()
                
                at_value = model.item(find_row_index, col_info.index('AtValue')).text()
                para_var= model.item(find_row_index, col_info.index('Para 변수')).text()
                kpd_func = model.item(find_row_index, col_info.index('KPD 함수')).text()
                default_val =  model.item(find_row_index, col_info.index('공장설정값')).text()
                max_val = model.item(find_row_index, col_info.index('최대값')).text()
                min_val = model.item(find_row_index, col_info.index('최소값')).text()
                form_msg = model.item(find_row_index, col_info.index('폼메시지')).text()
                unit = model.item(find_row_index, col_info.index('단위')).text()

                hidden_condition =  model.item(find_row_index, col_info.index('Hidden Con')).text()
                kpd_type = model.item(find_row_index, col_info.index('KPD 타입')).text()
                no_comm = model.item(find_row_index, col_info.index('통신쓰기금지')).text()
                read_only = model.item(find_row_index, col_info.index('읽기전용')).text()
                no_change_on_run =  model.item(find_row_index, col_info.index('운전중변경불가')).text()
                zero_input = model.item(find_row_index, col_info.index('0 입력가능')).text()
                '''
                no_comm, read_only, no_change_on_run, zero_input = False, False, False, False
                if( attribute & ATTR_NO_COMM ):
                    no_comm = True 
                if( attribute & ATTR_READ_ONLY ):
                    read_only = True
                if( attribute & ATTR_NO_CHANGE_ON_RUN ):
                    no_change_on_run = True 
                if( attribute & ATTR_ZERO_INPUT ):
                    zero_input = True 
                '''
                attribute = 0x0000
                if( no_comm == 'True'):
                    attribute |= ATTR_NO_COMM
                if( read_only == 'True'):
                    attribute |= ATTR_READ_ONLY
                if( no_change_on_run == 'True'):
                    attribute |= ATTR_NO_CHANGE_ON_RUN
                if( zero_input == 'True'):
                    attribute |= ATTR_ZERO_INPUT
                if( 'k_' in max_val ):
                    attribute |= ATTR_UP
                if( 'k_' in min_val ):
                    attribute |= ATTR_LP
                if( kpd_type == 'AfterEnter' ):
                    attribute |= ATTR_ENT
                hidden_val = self.hiddenConditionToValue(hidden_condition)
                attribute |= (hidden_val << 8)

                show_var  =  model.item(find_row_index, col_info.index('보임변수')).text()
                show_value = model.item(find_row_index, col_info.index('보임값')).text()
                eep_addr = model.item(find_row_index, col_info.index('EEP 주소')).text()
                comm_addr = model.item(find_row_index, col_info.index('통신주소')).text()
                max_eds = model.item(find_row_index, col_info.index('최대 EDS')).text()
                min_eds = model.item(find_row_index, col_info.index('최소 EDS')).text()
                comment = model.item(find_row_index, col_info.index('설명')).text()

                para_var = '(WORD*)&' + para_var
                default_val ='(WORD)' + default_val
                if( 'k_' in max_val ) :
                    max_val = '(LONG)&' + max_val
                else:
                    max_val = '(WORD)' + max_val

                if( 'k_' in min_val ) :
                    min_val = '(LONG)&' + min_val
                else:
                    min_val = '(WORD)' + min_val
                   
                if( unit == 'U_DATAMSG'):
                    form_msg = 'MSG_' + form_msg
                
                eds_val = ''
                if( max_eds or min_eds):
                    eds_val ='[EDS :{0},{1}]'.format(max_eds, min_eds)

                attribute_str = '0x{0:0>4}'.format(hex(attribute)[2:].upper())

                if( 'k_' in show_var or 'g_' in show_var ):
                    show_var = '(WORD*)&' + show_var

                format_str = '{{{0:<5},{1:<5},{2:<30},{3:<40},{4:<40},{5:<30},{6:<30},{7:<30},{8:<30},{9:<30},{10:<10},{11:<30},{12:<5}}},//"{13:<14}"{14}//{15}'

                if( find_item == find_items[-1]):
                    format_str = '{{{0:<5},{1:<5},{2:<30},{3:<40},{4:<40},{5:<30},{6:<30},{7:<30},{8:<30},{9:<30},{10:<10},{11:<30},{12:<5}}}//"{13:<14}"{14}//{15}'
                para_vars_lines.append(format_str.format \
                            (code_num, at_value, title_enum_name, para_var, kpd_func, default_val, max_val, min_val,
                            form_msg, unit, attribute_str, show_var, show_value, title_name, eds_val, comment)
                )
            
            para_vars.append(
                para_vars_template.format(group_name,
                                         group_name,
                                        '\n'.join(para_vars_lines))
            )
            para_vars_lines.clear()


        source_template = \
'''// PRQA S 502, 4130, 4131, 750, 759, 1514, 3218, 1504, 1505, 1503, 2860, 2895 EOF


/***********************************************
//  TABLE EDITOR 3  인버터 Keypad Table
//  Edit시 Table Edit 3 V2.00을 사용하세요      
***********************************************/
#include "BaseDefine.H"
#include "KPD_Title_Enum.H"
#include "KpdPara_GrpIdx.H"
#include "KpdPara_Msg.H"
#include "KpdPara_Vari.H"
#include "KpdPara_ShowParaVari.H"
#include "KFunc_Head.H"
#include "KpdPara_Table.H"
{0}
\n\n
static const S_GROUP_X_TYPE t_astGrpInfo[GROUP_TOTAL] = {{ 
{1}
}};\n\n
const S_GROUP_X_TYPE* KpdParaTableGetGrpAddr(WORD wGrpIdx)
{{
	return &t_astGrpInfo[wGrpIdx];
}}

const S_TABLE_X_TYPE* KpdParaTableGetTableAddr(WORD wGrpIdx, WORD wTableIdx)
{{
	const S_TABLE_X_TYPE* pstTable;

	switch(wGrpIdx)
	{{
{2}
	default:
		pstTable = NULL;
		break;
	}}
	return pstTable;
}}
'''
        file_contents = source_template.format( '\n'.join(para_vars),
                                                ',\n'.join(group_info_lines),
                                                ''.join(table_addr_lines)

        )
        TARGET_DIR = r"d:\download\1\result"
        with open(TARGET_DIR + os.path.sep + 'KpdPara_Table.c_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass


        header_template = \
'''#ifndef _KPD_TABLE_H
#define _KPD_TABLE_H
/***********************************************
//  TABLE EDITOR 3  인버터 Keypad Table
//  Edit시 Table Edit 3 V1.00을 사용하세요      
***********************************************/
#include "KpdPara_StructUnit.H"
\n\n
{0}\n\n
const S_GROUP_X_TYPE* KpdParaTableGetGrpAddr(WORD wGrpIdx);
const S_TABLE_X_TYPE* KpdParaTableGetTableAddr(WORD wGrpIdx, WORD wTableIdx);
\n\n
#endif   //_KPD_TABLE_H
'''
        file_contents = header_template.format(
            '\n'.join(defines_lines)
        )
        with open(TARGET_DIR + os.path.sep + 'KpdPara_Table.h_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass


        group_index_template = \
'''#ifndef KPDPARA_GRP_INDEX_H
#define KPDPARA_GRP_INDEX_H
\n
enum eGrpIndex{{
     {0}
	,GROUP_TOTAL
}};
\n
#endif   //KPDPARA_GRP_INDEX_H
'''

        file_contents = group_index_template.format(
            '\n\t,'.join(group_index_lines)
        )
        with open(TARGET_DIR + os.path.sep + 'KpdPara_grpidx.h_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass

    def make_kfunc_head(self):
        col_info = ci.para_col_info_for_view()
        model = self.model_parameters
        key_col_info = ci.group_col_info()
        key_model = self.model_group

        key_row = key_model.rowCount()

        cmd_key_func_lines = []
        after_enter_key_func_lines = []

        # key model 에서 key 값을 추출하여 key_value 모델에서 find 함 
        for row_index in range(key_row):
            # 그룹 정보 추출 
            key_group_name = key_model.item(row_index, key_col_info.index('Group')).text() 

            # 해당 하는 그룹의 아이템 정보를 얻음 
            find_items = model.findItems(key_group_name, column = col_info.index('Group'))

            key_func_list = [] # 중복 제거를 위해 사용 
            for find_item in find_items:
                find_row_index = find_item.row()

                key_func = model.item(find_row_index, col_info.index('KPD 함수')).text()
                code_num = model.item(find_row_index, col_info.index('Code#')).text()
                kpd_type = model.item(find_row_index, col_info.index('KPD 타입')).text()

                if('NULL' not in key_func):
                    if( key_func not in key_func_list ):
                        key_func_list.append(key_func)
                        arg = '{0:<40}//({1},{2:>2})'.format(key_func, key_group_name, code_num)
                        if(kpd_type == 'AfterEnter'):
                            after_enter_key_func_lines.append(arg)
                        else:
                            cmd_key_func_lines.append(arg)

        header_template = \
'''#ifndef KFUNC_INDEX_H
#define KFUNC_INDEX_H
\n
enum eKpdFuncIndex{{
	 KFUNC_NULL
    ,{0}
	,KFUNC_START_AFTER_ENT_FUNC = 1000
    ,{1}

}};
\n
#define TOTAL_KFUNC_CMD_ENT                  {2} 
#define TOTAL_KFUNC_AFTER_ENT                {3} 
\n
#endif   //KFUNC_INDEX_H
'''

        file_contents = header_template.format(
            '\n\t,'.join(cmd_key_func_lines),
            '\n\t,'.join(after_enter_key_func_lines),
            len(cmd_key_func_lines),
            len(after_enter_key_func_lines)
        )
        TARGET_DIR = r"d:\download\1\result"
        with open(TARGET_DIR + os.path.sep + 'KFunc_Head.h_temp', 'w', encoding='utf8') as f:
            f.write(file_contents)
        pass



if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('Table Editor 4')
    form.show()
    # form.make_kpdpara_var()
    # form.make_add_title_eng()
    # form.make_kpdpara_msg()
    # form.make_kpdpara_table()
    # form.make_kfunc_head()
    sys.exit(app.exec_())