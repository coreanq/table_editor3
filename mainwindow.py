import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui    import QStandardItemModel, QStandardItem
import mainwindow_ui 
import read_data as rd


class MainWindow(QMainWindow, mainwindow_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.modelGroup = QStandardItemModel(self)
        self.modelGroupInfo = QStandardItemModel(self)
        self.modelParameters = QStandardItemModel(self)
        self.initView()
        pass

    def readDataFromFile(self):
        TARGET_DIR = r'D:\download\1'
        for root, directories, filenames in os.walk(TARGET_DIR):
            # print(root, directories, filenames)
            for filename in filenames:
                try:
                    func = rd.parsing_file_func_dict[filename.lower()]
                    contents = ""
                    filePath = root + os.sep + filename
                    with open(filePath, 'r', encoding='utf8') as f:
                        contents = f.read()
                    for item in func(contents):
                        if(filename.lower() == rd.KPD_PARA_TABLE_SRC_FILE ):                                  
                            self.addRowToModel(self.modelParameters, item)
                            # print(item)
                            pass
                        elif( filename.lower() == rd.KPD_ADD_TITLE_SRC_FILE):
                            print(item)
                            pass
                        pass
                    pass
                except KeyError:
                    continue
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
        self.viewGroup.setModel(self.modelGroup)
        self.viewGroupInfo.setModel(self.modelGroupInfo)
        self.viewParameter.setModel(self.modelParameters) 
        
        # row 를 구분하기 위해서 번갈아 가면서 음영을 넣도록 함 
        for item in viewList:
            item.setAlternatingRowColors(True)

        pass

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = MainWindow()
    form.readDataFromFile()
    form.show()
    sys.exit(app.exec_())