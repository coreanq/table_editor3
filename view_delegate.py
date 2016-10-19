import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QStyledItemDelegate, QComboBox, QLineEdit
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp, Qt, QItemSelectionModel, QStringListModel
import util


class ViewDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ViewDelegate, self).__init__(parent)
        self.cols_info = {}
        pass

    def setEditorType(self, col, editor):
        self.cols_info.setdefault(col, {})['editor_type'] =  editor
        pass 

    def setModel(self, col, model):
        self.cols_info.setdefault(col, {} )['model'] = model
        pass

    def setEditable(self, col, editable ):
        self.cols_info.setdefault(col, {})['editable'] = editable
        pass
    
    def setValidator(self, col, validator):
        self.cols_info.setdefault(col, {})['validator'] = validator
        pass

    # { 1 : {'model': model, 'editable':editable }, ...}
    def createEditor(self, parent, option, index):
        # print(util.whoami() )
        col = index.column()
        row = index.row()
        col_info_dict = self.cols_info.get(col, {})

        model = col_info_dict.get('model', QStandardItemModel() )
        editable = col_info_dict.get('editable', False ) 
        editor_type = col_info_dict.get('editor_type', 'none')
        editor =  None

        if( editor_type == 'lineedit' ):
            editor = QLineEdit(parent)
            pass
        elif( editor_type == 'combobox'):
            editor = QComboBox(parent)
            editor.setModel(model)
            editor.setEditable(editable) 
            pass
        return editor

    def setEditorData(self, editor, index):
        # print(util.whoami() )
        text = index.model().data(index, Qt.EditRole) 

        col = index.column()
        row = index.row()
        col_info_dict = self.cols_info.get(col, {})
        editor_type = col_info_dict.get('editor_type', 'lineedit')

        if( editor_type == 'lineedit' ):
            editor.setText(text)
            pass
        elif( editor_type == 'combobox' ):
            index = editor.findText(text)
            editor.setCurrentText(text)
            pass
        pass 
        
    def setModelData(self, editor, model, index):
        # print(util.whoami() )
        col = index.column()
        row = index.row()
        col_info_dict = self.cols_info.get(col, {})
        editor_type = col_info_dict.get('editor_type', 'lineedit')

        if( editor_type == 'lineedit' ):
            text = editor.text()
            pass
        elif( editor_type == 'combobox' ):
            text = editor.currentText()
        print(type(model))
        model.setData(index, text, Qt.EditRole)
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

      