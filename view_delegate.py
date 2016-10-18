import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QStyledItemDelegate, QComboBox
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp, Qt, QItemSelectionModel, QStringListModel
import util


class ComboboxDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ComboboxDelegate, self).__init__(parent)
        self.model = None 
        self.editable = False
        pass
    def setModel(self, model):
        self.model = model
        pass
    def setEditable(self, editable ):
        self.editable = editable 
        pass

    def createEditor(self, parent, option, index):
        # print(util.whoami() )
        cmbBox = QComboBox(parent)
        cmbBox.setModel(self.model)
        cmbBox.setEditable(self.editable) 
        return cmbBox

    def setEditorData(self, editor, index):
        print(util.whoami() )
        text = index.model().data(index, Qt.EditRole) 
        try:
            index = editor.findText(text)
            editor.setCurrentText(text)
        except AttributeError:
            print( util.whoami() + "attribute error")
            return 
        pass 
    def setModelData(self, editor, model, index):
        # print(util.whoami() )
        try: 
            text = editor.currentText()
            model.setData(index, text, Qt.EditRole)
        except AttributeError:
            print ( util.whoami() + "attribute error")
            return  
        pass
    def updateEditorGemetry(self, editor, option, index):
        # print(util.whoami() )
        try:
            editor.setGeometry(option.rect)
        except:                
            print( util.whoami() + "attribute error")
        pass

      
class NoEditDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(NoEditDelegate, self).__init__(parent)
        pass

    def createEditor(self, parent, option, index):
        # print(util.whoami() )
        return None

    def setEditorData(self, editor, index):
        print(util.whoami() )
        return 
        pass 
    def setModelData(self, editor, model, index):
        print(util.whoami() )
        pass
    def updateEditorGemetry(self, editor, option, index):
        print(util.whoami() )
        editor.setGeometry(option.rect)

      