# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_design.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QStatusBar, QWidget)


class Ui_SlideShifter(object):
    def setupUi(self, SlideShifter):
        if not SlideShifter.objectName():
            SlideShifter.setObjectName(u"SlideShifter")
        SlideShifter.resize(400, 720)
        SlideShifter.setStyleSheet(u"background-color: rgb(70, 70, 70);\n"
                                   "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 230, 230, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 74), stop:0.425 rgba(255, 132, 132, 175), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));")
        self.centralwidget = QWidget(SlideShifter)
        self.centralwidget.setObjectName(u"centralwidget")
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(30, 320, 340, 150))
        self.start_button.setStyleSheet(u"background-color: rgb(120, 171, 101);\n"
                                        "font: 300 24pt \"Helvetica Neue\";\n"
                                        "color: rgb(0, 0, 0);")
        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(30, 490, 340, 150))
        self.stop_button.setStyleSheet(u"background-color: rgb(171, 55, 46);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 300 24pt \"Helvetica Neue\";")
        self.instruction_button = QPushButton(self.centralwidget)
        self.instruction_button.setObjectName(u"instruction_button")
        self.instruction_button.setGeometry(QRect(30, 149, 340, 150))
        self.instruction_button.setStyleSheet(u"background-color: rgb(138, 127, 122);\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "font: 300 24pt \"Helvetica Neue\";")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 30, 240, 50))
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 900 36pt \"Futura\";")
        SlideShifter.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(SlideShifter)
        self.statusbar.setObjectName(u"statusbar")
        SlideShifter.setStatusBar(self.statusbar)

        self.retranslateUi(SlideShifter)

        QMetaObject.connectSlotsByName(SlideShifter)

    # setupUi

    def retranslateUi(self, SlideShifter):
        SlideShifter.setWindowTitle(QCoreApplication.translate("SlideShifter", u"SlideShifter", None))
        self.start_button.setText(QCoreApplication.translate("SlideShifter", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("SlideShifter", u"Stop", None))
        self.instruction_button.setText(QCoreApplication.translate("SlideShifter", u"Instruction", None))
        self.label.setText(QCoreApplication.translate("SlideShifter", u"Slide Shifter", None))
    # retranslateUi
