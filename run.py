from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtWidgets

import sys
from main_window_design import Ui_SlideShifter

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Slide shifter")
        self.setGeometry(360, 150, 720, 720)

        self.window_text = QtWidgets.QLabel(self)
        self.window_text.setText('Чтобы начать нажмите кнопку "start"')
        self.window_text.move(250, 20)
        self.window_text.adjustSize()

        self.button = QtWidgets.QPushButton(self)
        self.button.setText('start')
        self.button.move(100, 200)
        self.button.setFixedWidth(200)
        self.button.setFixedHeight(100)
        self.button.clicked.connect(self.action)

    def action(self):
        print("some action")


def application():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_SlideShifter()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
