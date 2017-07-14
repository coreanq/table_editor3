import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import mainwindow
import version


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = mainwindow.MainWindow() 
    # widget = uic.loadUi("main_wnd.ui") # ide 에서 code completion 이 지원안되므로 사용안함 
    widget.resize(800, 600)
    widget.setWindowTitle('TableEditor4 V' + version.VERSION_INFO)
    widget.show()
    sys.exit(app.exec_())
