import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PyQt5.QtGui  import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QEvent, QObject
        
class ParameterViewKeyEater(QObject):
    sig_copy_clicked = pyqtSignal()
    sig_paste_clicked = pyqtSignal()
    sig_insert_clicked = pyqtSignal()
    sig_delete_clicked = pyqtSignal()
    
    def eventFilter(self, receiver, event):
        result = False
        if( event.type() == QEvent.KeyPress ):
            if( event.key() == Qt.Key_C and QApplication.keyboardModifiers() == Qt.ControlModifier ):
                self.sig_copy_clicked.emit()
                # print("control-c Key pressed")
                return True
            elif( event.key() == Qt.Key_V and QApplication.keyboardModifiers() == Qt.ControlModifier ):
                self.sig_paste_clicked.emit()
                # print("control-v Key pressed")
                return True
            elif( event.key() == Qt.Key_Insert):
                print("insert key pressed")
                self.sig_insert_clicked.emit()
                return True
            elif( event.key() == Qt.Key_Delete):
                print("delete key preseed") 
                self.sig_delete_clicked.emit()
                return True
            else:
                print(event.text() )
                return super(ParameterViewKeyEater, self).eventFilter(receiver, event)
        else:
            return super(ParameterViewKeyEater, self).eventFilter(receiver, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = QMainWindow()
    form.installEventFilter(ParameterViewKeyEater(form))
    form.show()
    sys.exit(app.exec_())

        