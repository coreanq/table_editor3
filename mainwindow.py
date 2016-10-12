import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp, Qt, QItemSelectionModel
import mainwindow_ui 
import view_key_eater as ve
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
        

        self.initView()
        self.createConnection()
        pass

    def createConnection(self):
        self.viewGroup.clicked.connect(self.onViewGroupClicked)  
        
        pass
    def initView(self):
        view_list = [self.viewGroup, self.viewGroupInfo, self.viewParameter, self.viewMessage, self.viewMessageValue]
        
        self.viewGroup.setModel(self.model_group)
        self.viewGroupInfo.setModel(self.model_group_info)
        self.model_proxy_parameters.setSourceModel(self.model_parameters)
        self.viewParameter.setModel(self.model_proxy_parameters) 
        
        self.viewMessage.setModel(self.model_msg)
        self.viewMessageValue.setModel(self.model_proxy_msg_values)
        self.model_proxy_msg_values.setSourceModel(self.model_msg_values)

        # row 를 구분하기 위해서 번갈아 가면서 음영을 넣도록 함 
        for item in view_list:
            item.setAlternatingRowColors(True)
            item.setSelectionBehavior(QAbstractItemView.SelectRows)
            item.setDragEnabled(True)
            item.setDragDropMode(QAbstractItemView.InternalMove)
            item.setDefaultDropAction(Qt.MoveAction)
            item.setSelectionMode(QAbstractItemView.SingleSelection)
            
        parameter_view_eater = ve.ParameterViewKeyEater(self)

        self.viewParameter.installEventFilter(parameter_view_eater)
        parameter_view_eater.sig_copy_clicked.connect(self.parameterViewCopyed)
        parameter_view_eater.sig_paste_clicked.connect(self.parameterViewPasted)
        parameter_view_eater.sig_insert_clicked.connect(self.parameterViewInserted)
        parameter_view_eater.sig_delete_clicked.connect(self.parameterViewDeleted)
        
    @pyqtSlot(QModelIndex)
    def onViewGroupClicked(self, index):
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
                        for item in rd.read_para_table(contents):
                            self.addRowToModel(self.model_parameters, item)
                        for item in rd.read_grp_info(contents):
                            self.addRowToModel(self.model_group, item)
                            pass
                        pass
                    elif( filename.lower() == rd.KPD_PARA_MSG_SRC_FILE):
                        for item in rd.read_para_msg(contents):
                            self.addRowToModel(self.model_msg_values, item)
                            print(item)
                            # self.addRowToModel()
                        # print(item)
                        pass
                    pass
                    pass
        pass
        
        
    def addRowToModel(self, model, datas):
        item_list = []
        for data in datas:
            item = QStandardItem(data)
            item_list.append(item)            
        model.appendRow(item_list)
        pass
    def insertRowToModel(self, model, datas, insert_index):
        item_list = []
        for data in datas:
            item = QStandardItem(data)
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