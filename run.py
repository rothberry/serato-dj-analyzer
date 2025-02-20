from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from ipdb import set_trace
from py_term_helpers import *
from lib.helper import FlaskHelper
import sys
import os
from app import create_app
from gui.template import Ui_MainWindow


# class MainWindow(QMainWindow):
class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Find stuff from template
        self.uploadBtn = self.findChild(QPushButton, "uploadBtn")
        self.uploadBtn.clicked.connect(self.open_dialog)

        self.playlistName = self.findChild(QTextBrowser, "playlistName")

    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "CSV (*.csv);; Txt (*.txt)",
        )
        playlist = FlaskHelper.parse_to_create(fname[0])
        set_trace()
        self.playlistName.setText(fname[0])
        print(fname)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        gui = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        gui.exec()
