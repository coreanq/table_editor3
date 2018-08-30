import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QStyledItemDelegate, QComboBox, QLineEdit
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor, QRegularExpressionValidator
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp, Qt, QItemSelectionModel, QStringListModel
import util


class ViewDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ViewDelegate, self).__init__(parent)
        self.cols_info = {}
        pass

    # { column :  {'model_colunm': 2, 'validator': ...} }
    def setEditorType(self, col, editor):
        self.cols_info.setdefault(col, {})['editor_type'] =  editor
        pass 
    
    # 입력으로 들어 오는 값이 숫자이면 formatting 하기 위함 
    def setEditorInputType(self, col, inputType):
        self.cols_info.setdefault(col, {})['input_type'] = inputType
        pass 
    # combobox 에서 모델로 삼을 column index 를 정해줌 
    def setModelColumn(self, col, cmb_model_column):
        self.cols_info.setdefault(col, {})['cmb_model_column'] = cmb_model_column
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
        validator = col_info_dict.get('validator', None) 
        editable = col_info_dict.get('editable', False ) 
        editor_type = col_info_dict.get('editor_type', 'none')
        cmb_model_column = col_info_dict.get('cmb_model_column', 0)
        editor =  None

        if( editor_type == 'lineedit' ):
            editor = QLineEdit(parent)
            if( validator ):
                editor.setValidator(QRegularExpressionValidator(validator))
            pass
        elif( editor_type == 'combobox'):
            editor = QComboBox(parent)
            editor.setModel(model)
            editor.setEditable(editable) 
            editor.setModelColumn(cmb_model_column)

        return editor

    def setEditorData(self, editor, index):
        # print(util.whoami() )
        text = index.model().data(index, Qt.EditRole) 

        col = index.column()
        row = index.row()
        col_info_dict = self.cols_info.get(col, {})
        editor_type = col_info_dict.get('editor_type', 'lineedit')
        input_type = col_info_dict.get('input_type', 'none')

        if( editor_type == 'lineedit' ):
            if( input_type == "number" ):
                # 우선 hex string, 나 단순 decimal string 오므로 integer 로 변환
                editor.setText( '{}'.format(int(text.replace(',', ''), 0 )) )
                pass
            else:
                editor.setText(text)
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
        input_type = col_info_dict.get('input_type', 'none')
        text = ""

        if( editor_type == 'lineedit' ):
            if( input_type == "number" ):
                # 우선 hex string, 나 단순 decimal string 오므로 integer 로 변환
                text = format(int(editor.text(), 0), ",")
            else:
                text = editor.text()
            pass
        elif( editor_type == 'combobox' ):
            text = editor.currentText()
        # print(type(model))
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

      