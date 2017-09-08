import os, sys, shutil, re, json, copy
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView,  \
                            QAction, QFileDialog, QMessageBox, QMenu
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor, QBrush 
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, \
                         QRegExp, Qt, QItemSelectionModel, QItemSelection,  QStringListModel,\
                         QFile, QObject, QEvent, QRegularExpression

import mainwindow_ui 
import proxy_model
import kpd_vari_changer as kc

import view_delegate as cbd 
import view_key_eater as ve
import column_info as ci
import read_data as rd
import resource_rc
import util
import version
import make_files as mk 

CONFIG_FILE_NAME = "TableEditor4_config.json"
CONFIG = {}

class CloseEventEater(QObject):
    def eventFilter(self, obj, event):
        if( event.type() == QEvent.Close):
            file_contents = json.dumps(CONFIG, ensure_ascii= False, indent=2)
            with open(os.path.curdir + os.path.sep + CONFIG_FILE_NAME, 'w', encoding='utf8' ) as f:
                f.write(file_contents)
            return True
        else:
            return super(CloseEventEater, self).eventFilter(obj, event)

class MainWindow(QMainWindow, mainwindow_ui.Ui_MainWindow):
    sigFileVersionChanged  = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.model_group = QStandardItemModel(self)
        self.model_proxy_group = QSortFilterProxyModel(self)

        self.model_parameters = QStandardItemModel(self)
        self.model_proxy_parameters = QSortFilterProxyModel(self)
        self.model_proxy_parameters_detail = proxy_model.ColumnProxyModel(self)
        # self.model_proxy_parameters_detail = QSortFilterProxyModel(self)
        
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

        self.actionAddGroup = QAction('Add Group', self)
        self.actionAddPara = QAction('Add Parameter', self)
        self.actionAddMsgInfo = QAction('Add MsgInfo', self)
        self.actionAddMsg = QAction('Add Msg', self)
        self.actionAddVar = QAction('Add Var', self )
        self.actionAddTitle = QAction('Add Title', self)

        self.view_list = [  self.viewGroup,  
                            self.viewParameter, self.viewMsgInfo, 
                            self.viewMsgValue,  
                            self.viewTitle]

        self.model_list = [
                            self.model_msg_info, 
                            self.model_msg_values,
                            self.model_parameters, 
                            self.model_group,
                            self.model_var,
                            self.model_title
        ]

        self.table_editor_number = ''
        self.table_editor_version = ''

        self.initModelAndView()
        self.createConnection()
        self.createAction()
        if( os.path.isfile(CONFIG_FILE_NAME) == True):
            with open(CONFIG_FILE_NAME, 'r', encoding='utf8') as f:
                file_contents = f.read()
                jsonConfig = json.loads(file_contents)
                global CONFIG
                CONFIG = copy.deepcopy(jsonConfig)
                if( '최근폴더' in jsonConfig ):
                    self.lineSourcePath.setText(jsonConfig['최근폴더'])
                
        source_path = self.lineSourcePath.text()
        if( source_path != ''):
            self.onOpen(source_path)
        pass

    def createConnection(self):
        self.btnCheck.clicked.connect(self.btnCheckClicked)

        self.viewGroup.selectionModel().currentChanged.connect(self.onViewGroupSelectionChanged)
        # self.viewGroup.clicked.connect(self.onViewGroupClicked)  
        self.viewMsgInfo.selectionModel().currentChanged.connect(self.onViewMsgInfoSelectionChanged)
        self.viewParameter.selectionModel().currentChanged.connect(self.onViewParameterSelectionChanged)
        
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

        # parametere view  더블 클릭시 unit의 msg combobox 내용을 변경하기 위함  
        self.viewParameter.doubleClicked.connect(self.onViewParameterDoubleClicked)
        self.model_parameters.dataChanged.connect(self.onModelParameterDataChanged)

        self.menuFile.triggered[QAction].connect(self.onMenuFileActionTriggered)
        self.menuEdit.triggered[QAction].connect(self.onMenuEditActionTriggered)
        self.menuAbout.triggered[QAction].connect(self.onMenuAboutActionTriggered)

        def actionAddFunc(action_name):
            def inner():
                self.onAddActionTriggered(action_name)
            return inner 
        
        self.actionAddGroup.triggered.connect(actionAddFunc('Group'))
        self.actionAddPara.triggered.connect(actionAddFunc('Para'))
        self.actionAddMsgInfo.triggered.connect(actionAddFunc('MsgInfo'))
        self.actionAddMsg.triggered.connect(actionAddFunc('Msg'))
        self.actionAddVar.triggered.connect(actionAddFunc('Var'))
        self.actionAddTitle.triggered.connect(actionAddFunc('Title'))
        self.actionKpdVariChange.triggered.connect(actionAddFunc('KpdVariChange'))


        pass

        # keypad index column 이 변경된 경우 해당하는 model 데이터를 업데이트 시켜줘야함 
        self.model_parameters.dataChanged.connect( self.onParameterModelChanged )
        self.model_parameters.modelReset.connect( self.onParameterModelChanged )
        self.model_parameters.rowsInserted.connect( self.onParameterModelChanged )
        self.model_parameters.rowsMoved.connect( self.onParameterModelChanged )
        self.model_parameters.rowsRemoved.connect( self.onParameterModelChanged )

    @pyqtSlot()
    def onParameterModelChanged(self):
        # print(util.whoami())
        pass

    def initView(self):
        view_list = self.view_list

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
        view.setColumnHidden( col_info.index('TitleIndex'), True )
        # view.setColumnHidden( col_info.index('ParaVar'), True )
        # view.setColumnHidden( col_info.index('KpdFunc'), True )
        # view.setColumnHidden( col_info.index('최대 EDS'), True )
        # view.setColumnHidden( col_info.index('최소 EDS'), True )


        # parameter view detail init
        # view = self.viewParameterDetail
        # self.model_proxy_parameters_detail.setSourceModel(self.model_parameters)
        # view.setModel(self.model_proxy_parameters_detail) 

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
        view.setColumnHidden(col_info.index('MsgComment'), True)
        view.setColumnHidden(col_info.index('TitleIndex'), True )
        

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
            verticalHeaderView.setHidden(True)
        
        # 특수 세팅
        self.viewParameter.setSelectionMode(QAbstractItemView.ExtendedSelection)
    def check_if_model_valid(self):

        # TODO: model valid 한지 파악 필요 
        # for model in self.model_list:
        #     row_cnt = model.rowCount()
        #     col_cnt = model.columnCount()
        #     for row in range(row_cnt):
        #         for col in range(col_cnt):
        #             item = model.item(row, col)
        #             if( item.text() == '' )


        pass
    
    def setFileVersion(self, table_editor_number, table_editor_version):
        self.table_editor_number = table_editor_number
        self.table_editor_version = table_editor_version 
        if( int(table_editor_number) == 0 ):
            self.lblVersion.setText('Table data is too old')
        else:
            self.lblVersion.setText('Table Editor ' + table_editor_number + '  Ver:'+ table_editor_version )
        self.sigFileVersionChanged.emit()
        pass

    @pyqtSlot(str)
    def onAddActionTriggered(self, action_name):
        if( action_name == 'Group'):
            model = self.model_group
            items = [QStandardItem() for x in range(len(ci.group_col_info()))]
            model.appendRow(items)
            pass
        # 왼쪽 창에서 선택한 행의 값을 기준으로 오른쪽창의 행을 추가 하기 위한 루틴 
        elif( action_name == 'Para'):
            model = self.model_parameters
            key_view = self.viewGroup
            items = [QStandardItem() for x in range(len(ci.para_col_info_for_view()))]

            selection_model = key_view.selectionModel()
            row_indexes = selection_model.selectedRows()

            if( len(row_indexes) == 0 ):
                QMessageBox.critical(self, '오류', '왼쪽 창에서 행이 선택 되지 않았습니다.')
                return  
            
            key_value = self.model_proxy_parameters.filterRegExp().pattern()
            key_value = key_value.replace('^', '')
            key_value = key_value.replace('$', '')
            items[ ci.para_col_info_for_view().index('Group')] = QStandardItem(key_value)
            model.appendRow(items)
            pass
        elif( action_name == 'MsgInfo'):
            model = self.model_msg_info
            items = [QStandardItem() for x in range(len(ci.msg_info_col_info()))]
            model.appendRow(items)
            pass
        # 왼쪽 창에서 선택한 행의 값을 기준으로 오른쪽창의 행을 추가 하기 위한 루틴 
        elif( action_name == 'Msg'):
            model = self.model_msg_values
            key_view = self.viewMsgInfo
            items = [QStandardItem() for x in range(len(ci.msg_values_col_info()))]

            selection_model = key_view.selectionModel()
            row_indexes = selection_model.selectedRows()

            if( len(row_indexes) == 0 ):
                QMessageBox.critical(self, '오류', '왼쪽 창에서 행이 선택 되지 않았습니다.')
                return  
            
            key_value = self.model_proxy_msg_values.filterRegExp().pattern()
            key_value = key_value.replace('^', '')
            key_value = key_value.replace('$', '')
            items[ ci.para_col_info_for_view().index('Group')] = QStandardItem(key_value)
            model.appendRow(items)
            pass
        elif( action_name == 'Var'):
            model = self.model_var
            items = [QStandardItem() for x in range(len(ci.variable_col_info()))]
            model.appendRow(items)
            pass
        elif( action_name == 'Title'):
            model = self.model_title
            items = [QStandardItem() for x in range(len(ci.title_col_info()))]
            model.appendRow(items)
            pass
        elif( action_name =='KpdVariChange'):
            current_path = self.lineSourcePath.text() 
            split_list = current_path.split('/')

            target_list = []
            for item in split_list:
                target_list.append(item)
                if( item == 'Source'):
                    break

            target_path = '/'.join(target_list)
            kc.chage_kpd_vari(self.model_parameters, target_path)
            print(util.whoami() )

        pass
    def createAction(self):
        view_list = self.view_list 
        for view in view_list:
            view.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.viewGroup.addAction(self.actionAddGroup)
        self.viewParameter.addAction(self.actionAddPara)
        self.viewMsgInfo.addAction(self.actionAddMsgInfo)
        self.viewMsgValue.addAction(self.actionAddMsg)
        self.viewTitle.addAction(self.actionAddTitle)
    
    def initModelAndView(self):
        self.model_msg_info.clear()
        self.model_msg_values.clear()
        self.model_kpd_para_unit.clear()
        self.model_parameters.clear()
        self.model_title.clear()
        self.model_var.clear()
        self.model_group.clear()
        
        self.initView()
        # 셀크기를 유지하기 위해 사용 
        self.initDelegate()

    def onOpen(self, dir_path):
        ret_val  = []
        
        if( not os.path.isdir(dir_path) ):
            ret_val.append('존재하지 않는 디렉토리')

        self.initModelAndView()

        ret, error_string = self.readDataFromFile(dir_path) 

        if( ret == False ):
            ret_val.append(error_string)

        if( len(ret_val) == 0 ):
            self.lineSourcePath.setText(dir_path)
            QMessageBox.information(self, '성공', '파일열기가 완료되었습니다')
            CONFIG['최근폴더']= dir_path

        else:
            self.initModelAndView()
            QMessageBox.critical(self, '실패', ' | '.join(ret_val))


        
    @pyqtSlot(QAction)
    def onMenuFileActionTriggered(self, action):
        action_type = action.text()
        current_path = self.lineSourcePath.text() 
        if( action_type == 'Open'):
            selected_dir = QFileDialog.getExistingDirectory(
                                            self, 
                                            caption = action_type, 
                                            directory = current_path, 
                                            options = QFileDialog.ShowDirsOnly
                                            )
            
            if( selected_dir == ''):
                return 
            self.onOpen(selected_dir)

            pass
        elif( action_type == 'Save'):
            ret_val = [] 
            source_path = self.lineSourcePath.text()

            if( not os.path.isdir(source_path) ):
                ret_val.append('소스 폴더명 오류')
            if(  self.make_backup_file(source_path) == False ):
                ret_val.append('백업 파일 생성 오류')
            
            if( len(ret_val) == 0 ):
                self.make_base_file(source_path) 
                self.make_model_to_file(source_path) 
                QMessageBox.information(self, '성공', '파일생성이 완료되었습니다')
            else:
                QMessageBox.information(self, '실패', ' | '.join(ret_val) )
            pass

        elif( action_type =='Save As'):
            ret_val = []
            selected_dir = QFileDialog.getExistingDirectory(
                                            self, 
                                            caption = action_type, 
                                            directory = current_path, 
                                            options = QFileDialog.ShowDirsOnly
                                            )
            
            if( not os.path.isdir(selected_dir) ):
                ret_val.append('소스 폴더명 오류')
            if( self.check_has_any_file_for_write(selected_dir) == True):
                ret_val.append('타겟 폴더에 중요 파일이 존재')
            if( self.model_parameters.rowCount() == 0 ):
                ret_val.append('데이터가 비어 있음')
            
            if( len(ret_val) == 0 ):
                self.make_base_file(selected_dir)
                self.make_model_to_file(selected_dir)
                QMessageBox.information(self, '성공', '파일생성이 완료되었습니다')
            else:
                QMessageBox.critical(self, '실패', ' | '.join(ret_val))
            pass

        elif( action_type == 'Exit'):
            exit()
            pass
       

    @pyqtSlot(QAction)
    def onMenuEditActionTriggered(self, action):
        widget = self.focusWidget()
        obj_name = widget.objectName()
        action_type = action.text()
        if( action_type == 'Copy'):
            if( obj_name == 'viewGroup' ):
                self.onGroupViewCopyed()
            elif( obj_name == 'viewParameter'):
                self.onParameterViewCopyed()
            elif( obj_name == 'viewMsgInfo'):
                self.onMsgInfoViewCopyed()
            elif( obj_name == 'viewMsgValue'):
                self.onMsgValueViewCopyed()
            elif( obj_name == 'viewVariable'):
                self.onVariableViewCopyed()
            elif( obj_name == 'viewTitle'):
                self.onTitleViewCopyed()
            pass
        elif( action_type == 'Paste'):
            if( obj_name == 'viewGroup' ):
                self.onGroupViewPasted()
            elif( obj_name == 'viewParameter'):
                self.onParameterViewPasted()
            elif( obj_name == 'viewMsgInfo'):
                self.onMsgInfoViewPasted()
            elif( obj_name == 'viewMsgValue'):
                self.onMsgValueViewPasted()
            elif( obj_name == 'viewVariable'):
                self.onVariableViewPasted()
            elif( obj_name == 'viewTitle'):
                self.onTitleViewPasted()
            pass
        elif( action_type == 'Insert'):
            if( obj_name == 'viewGroup' ):
                self.onGroupViewInserted()
            elif( obj_name == 'viewParameter'):
                self.onParameterViewInserted()
            elif( obj_name == 'viewMsgInfo'):
                self.onMsgInfoViewInserted()
            elif( obj_name == 'viewMsgValue'):
                self.onMsgValueViewInserted()
            elif( obj_name == 'viewVariable'):
                self.onVariableViewInserted()
            elif( obj_name == 'viewTitle'):
                self.onTitleViewInserted()
            pass
        elif( action_type == 'Delete'):
            if( obj_name == 'viewGroup' ):
                self.onGroupViewDeleted()
            elif( obj_name == 'viewParameter'):
                self.onParameterViewDeleted()
            elif( obj_name == 'viewMsgInfo'):
                self.onMsgInfoViewDeleted()
            elif( obj_name == 'viewMsgValue'):
                self.onMsgValueViewDeleted()
            elif( obj_name == 'viewVariable'):
                self.onVariableViewDeleted()
            elif( obj_name == 'viewTitle'):
                self.onTitleViewDeleted()
            pass

    @pyqtSlot(QAction)
    def onMenuAboutActionTriggered(self, action):
        print(action.text())

    
    def setLineDelegateAttribute(self, model, view, delegate, columns = [], validator = None):
        for col_index in columns:
            delegate.setEditable(col_index,  True ) 
            delegate.setEditorType(col_index, 'lineedit')
            if( validator ):
                delegate.setValidator(col_index, validator )
            view.setItemDelegateForColumn(col_index, delegate)
        pass

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
        col_index = col_info.index('CodeTITLE')
        cmb_model_column_index = ci.title_col_info().index('Title')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], width = 150, 
                cmb_model_column = cmb_model_column_index )

        model = self.model_kpd_para_unit
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_index = col_info.index('단위')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], editable = False,  width = 150)

        model = QStringListModel(['E_DATA_DIV_1','E_DATA_DIV_10', 'E_DATA_DIV_100','E_DATA_DIV_1K' , 'E_DATA_DIV_10K', 'E_DATA_DIV_100K'] ) 
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ 
            col_info.index('KpdWordScale'),
            col_info.index('KpdFloatScale')
        ]
        self.setCmbDelegateAttribute(model, view, delegate, col_indexes, editable = False,  
                width = 120 )

        model = QStringListModel( ['true', 'false']) 
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ 
            col_info.index('DataFunc실행여부'), 
            col_info.index('통신쓰기금지'), 
            col_info.index('읽기전용'),
            col_info.index('운전중변경불가'),
            col_info.index('0입력가능')
        ]
        self.setCmbDelegateAttribute(model, view, delegate, col_indexes )

        # code validator 설정
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ 
            col_info.index('Code#')
        ]
        reg_ex = QRegularExpression('[0-9]{1,2}')
        self.setLineDelegateAttribute(model, view, delegate, col_indexes, validator = reg_ex)

        # 공장 설정값 , 최대, 최소 validator 설정
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ 
            col_info.index('최대값'), 
            col_info.index('최소값'), 
            col_info.index('공장설정값')
        ]
        reg_ex = QRegularExpression('[0-9]{1,8}')
        self.setLineDelegateAttribute(model, view, delegate, col_indexes, validator = reg_ex)


        # 공장 설정값 , 최대, 최소 validator 설정
        view  = self.viewParameter
        delegate = self.delegate_parameters_view
        col_indexes = [ 
            col_info.index('Name')
        ]
        reg_ex = QRegularExpression('[A-Z]+[_A-Z0-9]*')
        self.setLineDelegateAttribute(model, view, delegate, col_indexes, validator = reg_ex)

        # group 설정 
        model = self.model_group
        view  = self.viewGroup
        delegate = self.delegate_group_view  
        col_info = ci.group_col_info()
        col_indexes = [ 
            col_info.index('Group')
        ]
        reg_ex = QRegularExpression('[A-Z]+[_A-Z0-9]*')
        self.setLineDelegateAttribute(model, view, delegate, col_indexes, validator = reg_ex) 

        # msg view delegate 설정 
        model = self.model_title
        view  = self.viewMsgValue
        delegate = self.delegate_msg_view  
        col_info = ci.msg_values_col_info()
        col_index = col_info.index('Title')
        cmb_model_column_index = ci.title_col_info().index('Title')
        self.setCmbDelegateAttribute(model, view, delegate, [col_index], width = 150, 
                cmb_model_column = cmb_model_column_index)

       
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

    @pyqtSlot()
    def btnCheckClicked(self):
        err_list = [] 
        grp_code_list = []
        name_list = []

        col_info = ci.para_col_info_for_view()
        grp_name_index = col_info.index('Group')
        code_index = col_info.index('Code#')
        name_index = col_info.index('Name')

        for row_index in range(self.model_parameters.rowCount()):
            grp_item = self.model_parameters.item(row_index, grp_name_index)
            code_item = self.model_parameters.item(row_index, code_index)
            name_item = self.model_parameters.item(row_index, name_index)

            loop_list = [grp_item, code_item, name_item ]
            for item in loop_list:
                item.setBackground(QBrush(QColor(Qt.white)))

            grp_code_list.append( '{}_{:0>2}'.format(grp_item.text() , code_item.text()) ) 
            name_list.append(name_item.text() )


        code_err_result_list = []
        name_err_result_list = []
        # code 중복 check 
        for row_index, value in enumerate(grp_code_list):
            if( grp_code_list.count(value) > 1 ):
                code_err_result_list.append( [row_index, value])

        for row_index, value in code_err_result_list:
            item = self.model_parameters.item(row_index, code_index)
            item.setBackground(QBrush(QColor(Qt.red)))

        # 변수 이름 중복 check 
        for row_index, value in enumerate(name_list):
            if( name_list.count(value) > 1 ):
                name_err_result_list.append( [row_index, grp_code_list[row_index]])

        for row_index, value in name_err_result_list:
            item = self.model_parameters.item(row_index, name_index)
            item.setBackground(QBrush(QColor(Qt.red)))
        pass

        if( len(code_err_result_list) or len (name_err_result_list)):
            QMessageBox.critical(self, '오류', '* code 오류: \n\t{}\n* name 오류:\n\t{}'.format( 
                '\n\t'.join([ x[1] for x in code_err_result_list] ),
                '\n\t'.join([ x[1] for x in name_err_result_list] )
                ))
            return code_err_result_list + name_err_result_list
        else:
            return [] 

    @pyqtSlot(QModelIndex, QModelIndex)
    def onViewGroupSelectionChanged(self, current, previous):
        # print(util.whoami() )
        row = current.row()
        col_info = ci.group_col_info()
        key_name = self.model_group.item(row, col_info.index('Group')).text() 
        regx = QRegExp('^' + key_name.strip() + '$' )  
        self.model_proxy_parameters.setFilterKeyColumn(0)
        self.model_proxy_parameters.setFilterRegExp(regx)
        pass
     
    @pyqtSlot(QModelIndex, QModelIndex)
    def onViewMsgInfoSelectionChanged(self, current, previous):
        # print(util.whoami() )
        row = current.row()
        col_info = ci.msg_info_col_info()
        key_name = self.model_msg_info.item(row, col_info.index('MsgName')).text()
        regx = QRegExp( '^' + key_name.strip() + '$' )
        self.model_proxy_msg_values.setFilterKeyColumn(0)
        self.model_proxy_msg_values.setFilterRegExp(regx)

    @pyqtSlot(QModelIndex, QModelIndex)
    def onViewParameterSelectionChanged(self, current, previous):
        src_model = self.model_proxy_parameters
        dst_model = self.model_proxy_parameters_detail
        dst_model.setSourceModel(self.viewParameter.selectionModel().model() )

        # src_row = current.row()
        # src_column = ci.para_col_info_for_view().index('Code#')

        # src_code_num_index = src_model.index(src_row, src_column)
        # src_code_num = src_model.data(src_code_num_index)
        # print(util.whoami() , src_row , src_code_num)
        # # 불필요 컬럼 hidden
        # for count in range(dst_model.columnCount() ):
        #     code_num = dst_model.data(dst_model.index(src_column, count)) 
        #     if( src_code_num == code_num ):
        #         self.viewParameterDetail.setColumnHidden(count, False)
        #     else:
        #         self.viewParameterDetail.setColumnHidden(count, True)
        pass
    def searchTitlefromEnumName(self, enumName):
        col_info = ci.title_col_info()
        items = self.model_title.findItems(enumName, column =col_info.index('Enum 이름'))
        for item in items:
            row = item.row()
            return self.model_title.item(row, col_info.index('Title')).text() 
        return ('')

    def makeAddrValue(self, group_num, code_num ):
        comm_addr = hex(0x1000 + (0x0100 * group_num) + code_num)
        comm_addr = '0x{0}'.format( comm_addr[2:].upper() )
        return comm_addr

    def make_backup_file(self, source_path):
        if( not os.path.exists(source_path) ) :
            return False

        target_path = source_path + '\\backup'
        if( not os.path.exists(target_path) ):
            os.mkdir(target_path)
        
        for file in rd.make_files:
            source_file_path = source_path + os.path.sep + file
            target_file_path = target_path + os.path.sep + file
            shutil.move(source_file_path, target_file_path)

        return True

    def make_base_file(self, source_path):
        #기본 키패드 title 파일이나, 기타 파일은 내부에서 리소스로 가지고 있다가 만들어줌 
        filelist = [rd.KPD_PARA_STRUCT_UNIT_HEADER_FILE , 
                    rd.KPD_BASIC_TITLE_SRC_FILE ]

        for file in filelist:
            resource_file_path = r':/base/' + file 
            source_file_path = source_path + os.path.sep + file 
            resource_fd = QFile(resource_file_path)
            contents = ''
            if( resource_fd.open(QFile.ReadOnly) == True ):
                contents = bytes(resource_fd.readAll()).decode('utf8')

                resource_fd.close()
            else:
                print("ERROR" + " " + resource_fd.errorString())
            
            with open(source_file_path, 'w', encoding= 'utf8') as f:
                f.write(str(contents))
        return True

    def make_model_to_file(self, source_path):
        mk.make_kpd_title(source_path, self.model_title)
        mk.make_kpdpara_msg(source_path, self.model_msg_info, self.model_msg_values)
        mk.make_kpdpara_table(source_path, self.model_parameters, self.model_group)
        mk.make_drv_para_data_storage(source_path, self.model_parameters)
        mk.make_drv_para_data_from_array(source_path, self.model_parameters)
        return True

    def check_has_any_file_for_write(self, source_path):
        ret = False 
        target_dir = source_path
        source_file_list  = []

        for (dirpath, dirnames, filenames) in os.walk(target_dir):
            source_file_list = filenames
            # root folder 만 확인할것이므로 바로 break 
            break
        source_file_list = [ file.lower() for file in source_file_list ]

        # writing 시 덮어 씌여지는 파일 있는지 체크  
        if( any ( x in source_file_list for x in rd.make_files) ):
            ret = True
        return ret

    def check_has_all_file_for_read(self, source_path):
        # 파싱에 필요한 모든 파일이 다 존재 하는지 확인 
        ret = False 
        error_string = '' 
        target_dir = source_path
        source_file_list  = []

        for (dirpath, dirnames, filenames) in os.walk(target_dir):
            source_file_list =list(map(str.lower, filenames))
            # root folder 만 확인할것이므로 바로 break 
            break
        # source_file_list = [ file.lower() for file in source_file_list ]

        expected_file_list = []
        for parsing_file_name in rd.parsing_files :
            if( not parsing_file_name.lower() in source_file_list ):
                expected_file_list.append(parsing_file_name)
            
        if( len(expected_file_list) ):
            error_string  = "타겟 폴더의 파일 리스트가 온전치 않음\n필요파일 리스트:\n" + '\n'.join(expected_file_list)
            ret = False
        else:
            ret = True 
        return ret, error_string

    # read_para_table 에서는 단순히 파일을 파싱해서 올려주는 역할만 하고 
    # 올라온 데이터에 대한 수정은 상위단에서 수행하도록 함 
    def readDataFromFile(self, source_path):
        target_dir = source_path
        source_file_list = []
        error_string = ''

        # 파싱에 필요한 모든 파일이 다 존재 하는지 확인 
        ret, error_string =  self.check_has_all_file_for_read(target_dir) 
        if( ret == False ):
            return ret, error_string 

        for filename in rd.parsing_files:
            file_path = target_dir + os.sep + filename 
            if( os.path.exists(file_path) ):
                contents = ""
                with open(file_path, 'r', encoding='utf8') as f:
                    contents = f.read()
                if(filename.lower() == rd.KPD_PARA_TABLE_SRC_FILE.lower() ):

                    # 테이블 버전 정보 얻기 
                    table_editor_number, table_editor_version = rd.read_para_table_version(contents)
                    self.setFileVersion(table_editor_number, table_editor_version)

                    # 그룹  정보 읽기 
                    for items in rd.read_grp_info(contents):
                        input_list = []
                        if( int(self.table_editor_number) < 4 ):
                            col_info = ci.group_col_info_old()
                            dummy_key = items[col_info.index('Dummy Key')]
                            group_name = items[col_info.index('Group')]

                        else:
                            col_info = ci.group_col_info()
                            dummy_key = items[col_info.index('Dummy Key')]
                            group_name = items[col_info.index('Group')]
                            # group_size = items[col_info.index('GroupSize')]

                        input_list = [dummy_key, group_name]
                        self.addRowToModel(self.model_group, input_list)
                        pass

                    # parameter table parameter 값 읽기 
                    is_new_table = True if int(self.table_editor_number) >= 4 else False 
                    for items in rd.read_para_table(contents, is_new_table):
                        col_info = None 

                        max_value, min_value =  '', ''

                        kpd_word_scale, kpd_float_scale = '', ''

                        group_name, code_name, name = '', '', ''

                        para_vari, kpd_func_name = '','' 
                        max_eds , min_eds = '', ''

                        comm_addr = ''

                        comment = ''

                        no_comm, read_only, no_change_on_run, zero_input = False, False, False, False

                        # col info 를 먼저 저장함 
                        if( int(self.table_editor_number) < 4 ):
                            col_info = ci.para_col_info_for_file_old()
                            self.actionKpdVariChange.setEnabled(True)
                        else:
                            col_info = ci.para_col_info_for_file()
                            self.actionKpdVariChange.setEnabled(False)

                        max_value = items[col_info.index('최대값')].upper()
                        min_value = items[col_info.index('최소값')].upper()

                        title = self.searchTitlefromEnumName(items[col_info.index('TitleIndex')])
                        at_value = items[col_info.index('AtValue')]
                        title = mk.make_title_with_at_value(title, at_value)

                        group_name = items[col_info.index('Group')]

                        # 파라미터 테이블 에디터 파일의 버전에 따라 읽는 방법을 변경한다. 
                        if( int(self.table_editor_number) < 4 ):
                            code_name = items[col_info.index('Code#')]
                            para_vari = items[col_info.index('ParaVar')]
                            kpd_func_name = items[col_info.index('KpdFunc')]

                            name = rd.changeParaName2Enum(para_vari)

                            kpd_word_scale = 'E_DATA_DIV_1'
                            kpd_float_scale = 'E_DATA_DIV_1'
                            max_eds = items[col_info.index('MaxEDS')]
                            min_eds = items[col_info.index('MinEDS')]

                            min_max_list = [min_value, max_value] 

                            # 이전 버전에는 min, max 에 변수가 들어 갔으므로 eds 적용해줌 
                            for count, value in enumerate(min_max_list):
                                ret = rd.re_parse_kpd_var_only.match(value)
                                if( ret and count == 0 ):
                                    min_value = min_eds
                                elif ( ret and count == 1):
                                    max_value = max_eds
                                    
                            comment = items[col_info.index('설명')]

                            # attribute 설정 
                            arg = items[col_info.index('Attribute')] 
                            if( arg == ''):
                                arg_num = 0
                            else:
                                arg_num = int(arg, 16)

                            attribute  = arg_num

                            if( attribute & mk.ATTR_NO_COMM ): no_comm = 'true' 
                            else: no_comm = 'false'

                            if( attribute & mk.ATTR_READ_ONLY ): read_only = 'true'
                            else: read_only = 'false'

                            if( attribute & mk.ATTR_NO_CHANGE_ON_RUN ): no_change_on_run = 'true' 
                            else: no_change_on_run = 'false'

                            if( attribute & mk.ATTR_ZERO_INPUT ): zero_input = 'true' 
                            else: zero_input = 'false'
                            find_items = self.model_group.findItems(group_name, column = ci.group_col_info().index('Group'))

                            # 한개만 찾아짐 
                            row = 0
                            for item in find_items:
                                row = item.row()
                                
                            comm_addr = self.makeAddrValue(row, int(code_name))

                        else:
                            name = items[col_info.index('Name')]
                            read_only = items[col_info.index('읽기전용')]
                            no_change_on_run = items[col_info.index('운전중변경불가')]
                            zero_input = items[col_info.index('0입력가능')]
                            no_comm = items[col_info.index('통신쓰기금지')]
                            comm_addr = items[col_info.index('통신주소')]
                            code_name = str(int(int(comm_addr, 0) & 0xff))
                            comment = items[-1]
                            

                        try : 
                            view_col_list = [ 
                                group_name,
                                code_name, 
                                name, 
                                items[col_info.index('TitleIndex')],
                                title, 
                                items[col_info.index('AtValue')], 
                                kpd_word_scale,
                                kpd_float_scale,
                                'true',
                                items[col_info.index('공장설정값')],
                                max_value,
                                min_value,
                                read_only, 
                                no_change_on_run , 
                                zero_input, 
                                no_comm, 
                                items[col_info.index('폼메시지')].replace('MSG_', ''),
                                items[col_info.index('단위')],
                                comm_addr,
                                comment
                            ]
                            # 에디팅 불가능하게 만드는 컬럼 리스트 
                            columns  = [ ci.para_col_info_for_view().index('통신주소')]
                            self.addRowToModel(self.model_parameters, view_col_list, editing_prohibit_columns = columns)
                        except IndexError:
                            print('error occur')
                            print(items)
                        

                elif( filename.lower() == rd.DRVPARA_DATASTORAGE_SRC_AUTO.lower() ):
                    for items in rd.read_data_storage_info(contents):   
                        key_column = ci.para_col_info_for_view().index('Name')
                        float_scale_column = ci.para_col_info_for_view().index('KpdFloatScale')
                        word_scale_column = ci.para_col_info_for_view().index('KpdWordScale')

                        name = items[ ci.data_storage_columns_info().index('Name') ]
                        float_scale = items[ ci.data_storage_columns_info().index('FloatScale') ]
                        word_scale = items[ ci.data_storage_columns_info().index('WordScale') ]

                        find_items = self.model_parameters.findItems(name, column = key_column)
                        find_row = 0
                        # 한개만 찾아짐 
                        for find_item in find_items:
                            find_row = find_item.row()
                        
                        self.model_parameters.setItem(find_row, float_scale_column, QStandardItem(float_scale) )
                        self.model_parameters.setItem(find_row, word_scale_column, QStandardItem(word_scale) )
                        pass
                    pass
                elif( filename.lower() == rd.KPD_PARA_MSG_SRC_FILE.lower()):
                    msg_list = [] 
                    col_info = ci.msg_values_col_info()
                    title_index = col_info.index('TitleIndex')
                    at_value_index = col_info.index('AtValue')
                    for items in rd.read_para_msg(contents):
                        msg_name = items[col_info.index('MsgName')]
                        msg_comment = items[col_info.index('MsgComment')]
                        msg_info = ['', msg_name, msg_comment ]

                        if( msg_info not in msg_list ):
                            msg_list.append(msg_info) 
                        title_enum  = items[title_index]
                        title = self.searchTitlefromEnumName(title_enum)
                        at_value = items[at_value_index]
                        title = mk.make_title_with_at_value(title, at_value )

                        insert_list =  msg_name, msg_comment, title_enum, title, at_value 
                        self.addRowToModel(self.model_msg_values, insert_list)
                        pass

                    for item in msg_list:
                        self.addRowToModel(self.model_msg_info, item)
                        
                elif( filename.lower() == rd.KPD_PARA_VAR_HEADER_FILE.lower() ):
                    for items in rd.read_kpd_para_var(contents):
                        self.addRowToModel(self.model_var, items)
                    pass
                elif ( filename.lower() == rd.KPD_BASIC_TITLE_SRC_FILE.lower() ):
                    for items in rd.read_basic_title(contents):
                        # 항상 add title 보다 앞서야 하므로 
                        self.addRowToModel(self.model_title, items, editing_prohibit_columns = list(range(len(items))) )
                    pass
                elif ( filename.lower() == rd.KPD_PARA_STRUCT_UNIT_HEADER_FILE.lower() ):
                    for items in rd.read_kpd_para_struct_unit(contents):
                        for item in items:
                            self.model_kpd_para_unit.appendRow(QStandardItem(item))

                elif ( filename.lower() == rd.KPD_ADD_TITLE_SRC_FILE.lower() ):
                    for items in rd.read_add_title(contents):
                        self.addRowToModel(self.model_title, items)
                pass
        return ret, error_string 
        pass

    def addRowToModel(self, model, data_list, editing_prohibit_columns =[] ):
        item_list = []
        for col_count, data in enumerate(data_list):
            item = QStandardItem(data)
            if( col_count in editing_prohibit_columns ):
                item.setBackground(QColor(Qt.lightGray) )
                item.setEditable(False)
            else:
                item.setEditable(True)

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

        if( unit_col  in range(topy, bottomy + 1) ):
            for row in range(topx, bottomx + 1):
                self.onParameterViewUnitChanged( self.model_parameters.index(row, unit_col )  )
            pass

    def viewRowCopy(self, subject, view):
        clipboard = QApplication.clipboard()
        view_model = view.model()
        selection_model = view.selectionModel()
        row_indexes = selection_model.selectedRows()
        data_dict = {}

        # multiline copy 가능 
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
        # view 의 model 은 proxy 모델이고 데이터를 추가 하기 위해서는 source model 이 필요함 
        clipboard = QApplication.clipboard()
        view_model = view.model() 
        key_value = view_model.filterRegExp().pattern() 
        key_value = key_value.replace('^', '')
        key_value = key_value.replace('$', '')
        current_index = view.currentIndex()

        source_index = view_model.mapToSource( current_index ) 
        insert_row = source_index.row() 
        dict_result = json.loads(clipboard.text())

        for key, lists in dict_result.items():
            # 동일한 항목의 데이터 복사 인지 확인 
            if( key == subject ):
                for row in lists:
                    row_items = row.split(',')
                    row_items[0] = key_value
                    self.insertRowToModel(source_model, row_items, insert_row)
                    insert_row = insert_row + 1
            break
        pass

    def viewRowInsert(self, view, source_model):
        # view 의 model 은 proxy 모델이고 데이터를 추가 하기 위해서는 source model 이 필요함 
        view_model = view.model() 
        key_value = view_model.filterRegExp().pattern() 
        key_value = key_value.replace('^', '')
        key_value = key_value.replace('$', '')
        current_index = view.currentIndex()

        source_index = view_model.mapToSource( current_index ) 
        insert_row = source_index.row() 

        row_items = [''] * view_model.columnCount()
        row_items[0] = key_value
        self.insertRowToModel(source_model, row_items, insert_row)
        pass

    def viewRowDelete(self, view):
        view_model = view.model()
        selection_model = view.selectionModel()
        row_indexes = selection_model.selectedRows()

        # 역순으로 row 제거해야함  
        for row_index in sorted(row_indexes, reverse =True ):
            view_model.removeRow(row_index.row())
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

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = MainWindow()
    # widget = uic.loadUi("main_wnd.ui") # ide 에서 code completion 이 지원안되므로 사용안함 
    closeEventEater = CloseEventEater()
    form.installEventFilter(closeEventEater)
    form.setWindowTitle('TableEditor4 V' + version.VERSION_INFO)
    form.show()
    sys.exit(app.exec_())