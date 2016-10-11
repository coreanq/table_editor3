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
        self.initView()
        self.createConnection()
        pass

    def createConnection(self):
        self.viewGroup.clicked.connect(self.onViewGroupClicked)  
        
        pass
        
    @pyqtSlot(QModelIndex)
    def onViewGroupClicked(self, index):
        row = index.row()
        column = index.column()
        grp_name = self.model_group.item(row, 0 ).text() 
        grp_name = grp_name.split('_')[1]
        regx = QRegExp(grp_name.strip()) 
        self.model_proxy_parameters.setFilterKeyColumn(0)
        self.model_proxy_parameters.setFilterRegExp(regx)
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
                    elif( filename.lower() == rd.KPD_ADD_TITLE_SRC_FILE):
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

    def initView(self):
        view_list = [self.viewGroup, self.viewGroupInfo, self.viewParameter]
        self.viewGroup.setModel(self.model_group)
        self.viewGroupInfo.setModel(self.model_group_info)
        self.model_proxy_parameters.setSourceModel(self.model_parameters)
        self.viewParameter.setModel(self.model_proxy_parameters) 
        
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
        
    @pyqtSlot()
    def parameterViewCopyed(self):
        clipboard = QApplication.clipboard()
        model = self.model_proxy_parameters
        s_model = self.viewParameter.selectionModel()
        row_indexes = []
        if(s_model.hasSelection() ):
            row_indexes = s_model.selectedRows()
        for row_index in row_indexes:
            row_data =  ','.join(model.data(model.index(row_index.row(), i) ) for i in range(model.columnCount() ) )
        print(row_data)

        clipboard.setText(row_data)
        pass
    @pyqtSlot()
    def parameterViewPasted(self):
        clipboard = QApplication.clipboard()
        model = self.model_proxy_parameters
        s_model = self.viewParameter.selectionModel()
        row_indexes = []
        insert_index = 0
        if(s_model.hasSelection() ):
            row_indexes = s_model.selectedRows()
            # 한개만 선택됨 
            for row_index in row_indexes:
                insert_index = model.maptoSource(row_index).row()
        else:
            insert_index = s_model.rowCount()
        datas = clipboard.text().split(',')
        row_items = [QStandardItem(data) for data in datas]
        model.insertRow(insert_index, row_items)

            

        print(row_data)
        pass 
    @pyqtSlot()
    def parameterViewInserted(self):
        pass
    def parameterViewDeleted(self):
        pass
    def groupViewCopyed(self):
        pass

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = MainWindow()
    form.readDataFromFile()
    form.show()
    sys.exit(app.exec_())