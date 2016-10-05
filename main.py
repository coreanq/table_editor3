import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
import read_data as rd
import main_wnd


if __name__ ==  '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(250, 150)
    w.show()
    sys.exit(app.exec_())
