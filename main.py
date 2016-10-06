import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import read_data as rd
import mainwindow

if __name__ == '__main__':
    print("Hello world")
    app = QApplication(sys.argv)
    widget = mainwindow.MainWindow() 

    # widget = uic.loadUi("main_wnd.ui")
    widget.resize(640, 480)
    widget.show()
    sys.exit(app.exec_())
