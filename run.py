from PySide6.QtWidgets import QApplication, QMainWindow

import sys
from window import Ui_SlideShifter
from main import hand_tracking_function


def application():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_SlideShifter()
    ui.setupUi(window)
    window.show()

    hand_tracking_function()

    sys.exit(app.exec())


if __name__ == "__main__":
    application()
