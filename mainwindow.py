import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PyQt5.QtGui  import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp 
import mainwindow_ui 
import read_data as rd


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
        viewList = [self.viewGroup, self.viewGroupInfo, self.viewParameter]
        self.viewGroup.setModel(self.model_group)
        self.viewGroupInfo.setModel(self.model_group_info)
        self.model_proxy_parameters.setSourceModel(self.model_parameters)
        self.viewParameter.setModel(self.model_proxy_parameters) 
        
        # row 를 구분하기 위해서 번갈아 가면서 음영을 넣도록 함 
        for item in viewList:
            item.setAlternatingRowColors(True)
            item.setSelectionBehavior(QAbstractItemView.SelectRows)
        pass

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = MainWindow()
    form.readDataFromFile()
    form.show()
    sys.exit(app.exec_())