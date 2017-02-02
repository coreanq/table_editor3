import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import read_data as rd
import mainwindow

VERSION_NUMBER = '0.0.0.5'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = mainwindow.MainWindow() 
    # widget = uic.loadUi("main_wnd.ui") # ide 에서 code completion 이 지원안되므로 사용안함 
    widget.resize(640, 480)
    widget.setWindowTitle('TableEditor4 ' + VERSION_NUMBER)
    widget.show()
    sys.exit(app.exec_())
