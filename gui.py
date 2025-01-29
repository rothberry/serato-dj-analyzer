from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from ipdb import set_trace
from py_term_helpers import *
from lib.helper import FlaskHelper
import sys
import os
from app import create_app


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        btn = QPushButton(self)
        btn.setText("Open file dialog")
        self.setCentralWidget(btn)
        btn.clicked.connect(self.open_dialog)

        self.label = QLabel()

    @pyqtSlot()
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


if __name__ == "__main__":

    app = create_app()
    with app.app_context():
        gui = QApplication(sys.argv)

        window = MainWindow()
        window.show()
        # Start the event loop.
        gui.exec()
