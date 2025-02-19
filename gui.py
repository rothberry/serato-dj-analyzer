from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from ipdb import set_trace
from py_term_helpers import *
from lib.helper import FlaskHelper
import sys
import os
from app import create_app
from output import Ui_MainWindow


# class MainWindow(QMainWindow):
class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.uploadBtn = self.findChild(QPushButton, "uploadBtn")
        print(self.uploadBtn.objectName())
        self.uploadBtn.clicked.connect(self.on_click)

        upB = self.findChild(QPushButton, "uploadBtn_2")
        print(upB.objectName())
        upB.clicked.connect(self.on_click)


    @pyqtSlot()
    def on_click(self):
        print("KAHGSFGHKASFDHGKADFSHGKDAFGHK")

    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "CSV (*.csv);; Txt (*.txt)",
        )
        FlaskHelper.parse_to_create(fname[0])
        set_trace()
        self.label.setText(fname)
        print(fname)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        gui = QApplication(sys.argv)
        window = MainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)
        window.show()
        gui.exec()
