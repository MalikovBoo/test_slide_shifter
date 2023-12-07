# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_design.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QLabel, QPushButton,
                               QWidget)

import main


class Ui_SlideShifter(object):
    def __init__(self):
        self.cnt = 0

    def setupUi(self, SlideShifter):
        if not SlideShifter.objectName():
            SlideShifter.setObjectName(u"SlideShifter")
        SlideShifter.resize(400, 720)
        SlideShifter.move(0, 0)
        SlideShifter.setStyleSheet(u"background-color: rgb(40, 40, 40);")
        self.centralwidget = QWidget(SlideShifter)
        self.centralwidget.setObjectName(u"centralwidget")
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(30, 210, 340, 150))
        self.start_button.setStyleSheet(u"background-color: rgb(107, 182, 84);\n"
                                        "font: 300 24pt \"Helvetica Neue\";\n"
                                        "color: rgb(0, 0, 0);")
        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(30, 370, 340, 150))
        self.stop_button.setStyleSheet(u"background-color: rgb(189, 54, 43);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 300 24pt \"Helvetica Neue\";")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 60, 240, 50))
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 900 36pt \"Futura\";")
        self.turn_on_off_button = QPushButton(self.centralwidget)
        self.turn_on_off_button.setObjectName(u"turn_on_off_button")
        self.turn_on_off_button.setGeometry(QRect(30, 530, 340, 70))
        self.turn_on_off_button.setStyleSheet(u"background-color: rgb(52, 120, 246);\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "font: 300 24pt \"Helvetica Neue\";")
        SlideShifter.setCentralWidget(self.centralwidget)

        self.retranslateUi(SlideShifter)

        QMetaObject.connectSlotsByName(SlideShifter)

        self.do_actions()

    # setupUi

    def retranslateUi(self, SlideShifter):
        SlideShifter.setWindowTitle(QCoreApplication.translate("SlideShifter", u"SlideShifterVideo", None))
        self.start_button.setText(QCoreApplication.translate("SlideShifter", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.stop_button.setText(QCoreApplication.translate("SlideShifter", u"\u0421\u0442\u043e\u043f", None))
        self.label.setText(QCoreApplication.translate("SlideShifter", u"Slide Shifter", None))
        self.turn_on_off_button.setText(QCoreApplication.translate("SlideShifter",
                                                                   u"\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u044c/\u0412\u044b\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0432\u0438\u0434\u0435\u043e",
                                                                   None))

    # retranslateUi

    def do_actions(self):
        self.start_button.clicked.connect(self.start_hand_tracking)
        self.stop_button.clicked.connect(self.stop_hand_tracking)
        self.turn_on_off_button.clicked.connect(self.turn_on_off_video)

    def start_hand_tracking(self):
        main.is_started = True

    def stop_hand_tracking(self):
        main.is_started = False

    def turn_on_off_video(self):
        self.cnt += 1
        if self.cnt % 2 == 0:
            main.video_on = True
        else:
            main.video_on = False
        main.hand_tracking_function()
