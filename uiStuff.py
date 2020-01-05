"""This code is used to initialise PyQt and enable display of user Interface"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from DesignerCode import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)

window = QMainWindow()
ui = Ui_MainWindow()

ui.setupUi(window)



