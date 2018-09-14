import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QStyledItemDelegate, QComboBox, QLineEdit, QCompleter
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QClipboard, QColor, QRegularExpressionValidator
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRegExp, Qt, QItemSelectionModel, QStringListModel, QEvent
import util


class ViewDelegate(QStyledItemDelegate):

    sigDataChanged  = pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(ViewDelegate, self).__init__(parent)
        self.cols_info = {}
        self.old_data = ""
        self.new_data = ""
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

    @pyqtSlot(str)
    def onCmbBoxEditTextChanged(self, str):
        
        pass

    # 각 컬럼마다 model, editiable 정보를 담고 있다 
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
            # def generate_func(model):
            #     @pyqtSlot(str)
            #     def inner_func(str):
            #         # model.setFilterRegExp("{}".format(str))
            #         print(str)
            #     return inner_func
            # func = generate_func(model) 
            completer = QCompleter(self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            editor.setCompleter(completer)

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

        input_data = ''

        if( editor_type == 'lineedit' ):
            if( input_type == "number" ):
                # 우선 hex string, 나 단순 decimal string 오므로 integer 로 변환
                if( text != "" ) :
                    input_data =  '{}'.format(int(text.replace(',', ''), 0 )) 
                else:
                    input_data = "0"
            else:
                input_data = text
            editor.setText(input_data)

        elif( editor_type == 'combobox' ):
            input_data = text
            editor.setCurrentText(input_data)

        if( self.old_data == ''):
            # 에디트 하기 전 초기 값을 얻어와서 old -> new 가 어떻게 변했는지 알기 위함 이름 변경 시 사용하기 위함  
            self.old_data = input_data
        
    def setModelData(self, editor, model, index):
        # print(util.whoami() )
        col = index.column()
        row = index.row()
        col_info_dict = self.cols_info.get(col, {})
        editor_type = col_info_dict.get('editor_type', 'lineedit')
        input_type = col_info_dict.get('input_type', 'none')

        input_data = ''

        if( editor_type == 'lineedit' ):
            if( input_type == "number" ):
                # 우선 hex string, 나 단순 decimal string 오므로 integer 로 변환
                input_data = editor.text()
                if( input_data != ""):
                    input_data = format(int(input_data, 0), ",")
                else:
                    input_data = "0"
            else:
                input_data = editor.text()
            pass
        elif( editor_type == 'combobox' ):
            input_data = editor.currentText()
        # print(type(model))
        if( input_data == ""):
            model.setData(index, self.old_data, Qt.EditRole)
        else:
            model.setData(index, input_data, Qt.EditRole)

        self.new_data = input_data
        self.sigDataChanged.emit(self.old_data, self.new_data)
        # 초기화 
        self.old_data = ''
        self.new_data = ''
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

      