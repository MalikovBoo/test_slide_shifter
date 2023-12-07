from PySide6.QtWidgets import QApplication, QMainWindow

import sys
from window import UiSlideShifter
from main import start_hand_tracking


def application():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = UiSlideShifter()
    ui.setup_ui(window)
    window.show()

    start_hand_tracking()

    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
