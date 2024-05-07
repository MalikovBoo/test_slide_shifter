import cv2
import mediapipe
import math
import pyautogui
import sys
import time
import traceback

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
                               QPushButton, QTextEdit, QWidget, QMessageBox, QGridLayout)


class UiSlideShifter(QMainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, SlideShifter):
        """Show User Interface"""

        if not SlideShifter.objectName():
            SlideShifter.setObjectName(u"SlideShifter")

        SlideShifter.move(0, 0)
        SlideShifter.resize(400, 720)
        SlideShifter.setStyleSheet(u"background-color: rgb(50, 50, 50);")
        self.centralwidget = QWidget(SlideShifter)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        self.label_camera = QLabel(self.centralwidget)
        self.label_camera.setObjectName(u"label_camera")
        self.label_camera.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                        "color: rgb(211, 213, 213);\n"
                                        "font: 400 16pt \"Helvetica Neue\";\n")
        self.gridLayout.addWidget(self.label_camera, 0, 0, 1, 1)

        self.comboBox_camera = QComboBox(self.centralwidget)
        self.comboBox_camera.setObjectName(u"comboBox_camera")
        self.comboBox_camera.setStyleSheet(u"background-color: rgb(32, 32, 32);\n"
                                           "color: rgb(229, 231, 231);\n"
                                           "font: 300 14pt \"Helvetica Neue\";")
        self.gridLayout.addWidget(self.comboBox_camera, 2, 0, 1, 1)

        self.label_tracking = QLabel(self.centralwidget)
        self.label_tracking.setObjectName(u"label_tracking")
        self.label_tracking.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                          "color: rgb(211, 213, 213);\n"
                                          "font: 400 16pt \"Helvetica Neue\";\n")
        self.gridLayout.addWidget(self.label_tracking, 0, 2, 1, 1)

        self.comboBox_tracking = QComboBox(self.centralwidget)
        self.comboBox_tracking.setObjectName(u"comboBox_tracking")
        self.comboBox_tracking.setStyleSheet(u"background-color: rgb(32, 32, 32);\n"
                                             "color: rgb(229, 231, 231);\n"
                                             "font: 300 14pt \"Helvetica Neue\";")
        options_to_track = ["Двух рук", "Правой руки", "Левой руки"]
        for i in range(3):
            self.comboBox_tracking.addItem("")
            self.comboBox_tracking.setItemText(i, QCoreApplication.translate("SlideShifter", options_to_track[i], None))
        self.gridLayout.addWidget(self.comboBox_tracking, 2, 2, 1, 1)

        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setStyleSheet(u"background-color: rgb(123, 178, 113);\n"
                                        "font: 400 24pt \"Helvetica Neue\";\n"
                                        "color: rgb(0, 0, 0);")
        self.gridLayout.addWidget(self.start_button, 4, 0, 1, 6)

        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setStyleSheet(u"background-color: rgb(220, 72, 60);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 400 24pt \"Helvetica Neue\";")
        self.gridLayout.addWidget(self.stop_button, 5, 0, 1, 6)

        self.label_slide = QLabel(self.centralwidget)
        self.label_slide.setObjectName(u"label_slide")
        self.label_slide.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                       "color: rgb(247, 249, 249);\n"
                                       "font: 900 34pt \"Futura\";")
        self.gridLayout.addWidget(self.label_slide, 3, 1, 1, 1)

        self.label_shifter = QLabel(self.centralwidget)
        self.label_shifter.setObjectName(u"label_shifter")
        self.label_shifter.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                         "color: rgb(116, 170, 255);\n"
                                         "font: 900 34pt \"Futura\";")
        self.gridLayout.addWidget(self.label_shifter, 3, 2, 1, 1)

        self.log_text_edit = QTextEdit(self.centralwidget)
        self.log_text_edit.setObjectName(u"log_text_edit")
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setStyleSheet(u"background-color: rgb(32, 32, 32);\n"
                                         "color: rgb(229, 231, 231);\n"
                                         "font: 300 16pt \"Helvetica Neue\";")
        self.gridLayout.addWidget(self.log_text_edit, 6, 0, 1, 6)

        self.label_by = QLabel(self.centralwidget)
        self.label_by.setObjectName(u"label_by")
        self.label_by.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                    "color: rgb(156, 158, 158);\n"
                                    "font: 600 16pt \"Futura\";\n")
        self.gridLayout.addWidget(self.label_by, 7, 0, 1, 1, Qt.AlignRight)

        self.label_singularity = QLabel(self.centralwidget)
        self.label_singularity.setObjectName(u"label_singularity")
        self.label_singularity.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                             "color: rgb(224, 226, 226);\n"
                                             "font: 600 16pt \"Futura\";\n")
        self.gridLayout.addWidget(self.label_singularity, 7, 1, 1, 1, Qt.AlignRight)

        self.label_hub = QLabel(self.centralwidget)
        self.label_hub.setObjectName(u"label_hub")
        self.label_hub.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                     "color: rgb(92, 156, 255);\n"
                                     "font: 600 16pt \"Futura\";\n")
        self.gridLayout.addWidget(self.label_hub, 7, 2, 1, 1, Qt.AlignLeft)

        SlideShifter.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(SlideShifter)

        self.retranslateUi(SlideShifter)
        self.get_connected_cameras()
        self.connect_buttons()

    def retranslateUi(self, SlideShifter):
        SlideShifter.setWindowTitle(QCoreApplication.translate("SlideShifter", "Slide Shifter", None))
        self.label_camera.setText(QCoreApplication.translate("SlideShifter", "Камера", None))
        self.label_tracking.setText(QCoreApplication.translate("SlideShifter", "Отслеживание", None))
        self.label_slide.setText(QCoreApplication.translate("SlideShifter", "Slide", None))
        self.label_shifter.setText(QCoreApplication.translate("SlideShifter", "Shifter", None))
        self.start_button.setText(QCoreApplication.translate("SlideShifter", "Начать", None))
        self.stop_button.setText(QCoreApplication.translate("SlideShifter", "Приостановить", None))
        self.label_by.setText(QCoreApplication.translate("SlideShifter", "by", None))
        self.label_singularity.setText(QCoreApplication.translate("SlideShifter", "Singularity", None))
        self.label_hub.setText(QCoreApplication.translate("SlideShifter", "Hub", None))

    def connect_buttons(self):
        """Activate buttons"""

        self.comboBox_camera.activated.connect(self.activate_camera)
        self.comboBox_tracking.activated.connect(self.choosing_hand_to_track)
        self.start_button.clicked.connect(self.start_hand_tracking)
        self.stop_button.clicked.connect(self.stop_hand_tracking)

    def get_connected_cameras(self):
        """Get the ID of all cameras connected to the PC"""

        cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if not cap.isOpened():
                break
            cameras.append(i)
            cap.release()
            self.comboBox_camera.addItem("")
            self.comboBox_camera.setItemText(i, QCoreApplication.translate("SlideShifter", f"№{i + 1}", None))
        ht.cameras = cameras

    def activate_camera(self, index: int):
        """Selecting a camera for hand tracking"""

        ht.camera_index = index
        ht.hand_tracking_function()

    def choosing_hand_to_track(self, index: int):
        """Choosing hand to track"""

        if index == 0:
            ht.hand_to_track = None
        elif index == 1:
            ht.hand_to_track = "Right"
        elif index == 2:
            ht.hand_to_track = "Left"

    def start_hand_tracking(self):
        """Hand tracing start"""

        ht.is_started = True
        text_for_log = "Включено отслеживание рук"
        self.append_to_log(self.format_text_with_color(text=text_for_log, color="orange"))

    def stop_hand_tracking(self):
        """Hand tracking suspension"""

        # Stop hand tracking function
        ht.is_started = False
        text_for_log = "Приостановлено отслеживание рук"
        self.append_to_log(self.format_text_with_color(text=text_for_log, color="orange"))

    def format_text_with_color(self, text: str, color: str):
        """Converting text into html format"""

        colors = {
            "white": "e0e2e2",
            "blue": "5c9cff",
            "green": "6e9664",
            "red": "dc483c",
            "grey": "9c9e9e",
            "pink": "e8b0e8",
            "yellow": "ede59d",
            "orange": "ff7f50",
        }
        if color not in colors.keys():
            color = "white"
        return f"<font color='#{colors[color]}'>{text}</font><br>"

    def append_to_log(self, text: str):
        """Displaying the message in the logging field"""

        self.log_text_edit.insertHtml(text)
        self.log_text_edit.verticalScrollBar().setValue(self.log_text_edit.verticalScrollBar().maximum())

    def closeEvent(self, event):
        """Displaying the application close window """

        # Handle close event for the main window
        reply = self.show_quit_confirmation_dialog()
        if reply == QMessageBox.Yes:
            event.accept()
            ht.is_video_on = False
            sys.exit(0)
        else:
            event.ignore()

    def show_quit_confirmation_dialog(self):
        """Get yes or no when person want to close application"""

        exit_answer = QMessageBox.question(self, "Подтверждение закрытия",
                                           "Закрыть приложение?",
                                           QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        return exit_answer

    def show_error_message(self, text: str):
        """Displaying the exit window in case of an error"""

        message_box = QMessageBox()
        message_box.setWindowTitle("Error window")
        message_box.setText(text)
        message_box.addButton(QMessageBox.Ok)
        message_box.exec()

        ht.is_video_on = False
        sys.exit(1)


class HandDetector:
    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.lm_list = []  # List to store coordinates of hands landmarks
        self.results = None  # Collection of tracked hands; include:(multi_hand_landmarks, multi_handedness)
        self.mp_hands = mediapipe.solutions.hands
        self.hands = self.mp_hands.Hands(mode, max_hands, model_complexity, detection_con, track_con)

    def find_hands(self, image, draw=True):
        """Look for hands in the picture"""

        if image is None:
            return None

        mp_draw = mediapipe.solutions.drawing_utils
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return image

    def find_position(self, image, exact_hand=None, draw=True):
        """On the founded hands draw their dots and a frame"""

        if exact_hand is not None and exact_hand not in ["Right", "Left"]:
            exact_hand = None

        self.lm_list = []

        if self.results.multi_hand_landmarks:
            for i in range(len(self.results.multi_hand_landmarks)):
                label = self.results.multi_handedness[i].classification[0].label

                if label == exact_hand or exact_hand is None:
                    hand = self.results.multi_hand_landmarks[i]
                    x_list = []
                    y_list = []
                    hand_lm = []

                    for id, lm in enumerate(hand.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        x_list.append(cx)
                        y_list.append(cy)
                        hand_lm.append([id, cx, cy])
                        if draw:
                            cv2.circle(image, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    frame = [min(x_list), min(y_list), max(x_list), max(y_list)]
                    self.lm_list.append(hand_lm)
                    if draw:
                        cv2.rectangle(image, (frame[0] - 20, frame[1] - 20), (frame[2] + 20, frame[3] + 20),
                                      (0, 255, 0), 2)
        return self.lm_list

    def find_distance(self, hand: int, index1: int, index2: int, image, draw=True):
        """Find the distance between points on the hand"""

        lm_list = self.lm_list[hand]
        x1, y1 = lm_list[index1][1], lm_list[index1][2]
        x2, y2 = lm_list[index2][1], lm_list[index2][2]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if draw:
            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length


class HandTracking:
    def __init__(self):
        self.video_window_title = "Slide Shifter Video"
        self.is_video_on = True
        self.is_started = False
        self.hand_to_track = None  # "Left" or "Right" or None
        self.cameras = []
        self.camera_index = 0
        self.detector = HandDetector(detection_con=0.8)

        self.is_slide_switched = [False, False]
        self.start_thumb_position = [None, None]  # Start x-thumb position of left and right hands
        self.start_gesture_time = [None, None]  # Start time of holding the left and right hand gesture
        self.gesture_time_threshold = 0.3  # Threshold for holding the gesture in one position (seconds)
        self.ready_to_slide = [False, False]  # Is the right and left hand gesture ready to flip the slide
        self.marker_to_print = [0, 0]  # A marker that helps you display the readiness to flip the slide exactly 1 time
        self.slides_to_switch = [0, 0]
        self.start_count_time = [None, None]
        self.count_time_threshold = 2
        self.count_or_not = [True, True]

        self.length_in_normal_position = None
        self.length_in_gesture = None
        self.start_time_to_setup_positions = None

    def find_x_coordinate_of_thumbs(self, landmarks: list):
        """Finding the x-coordinate of the thumbs"""

        try:
            first_hand = landmarks[0]
            x1 = first_hand[4][1]
        except IndexError:
            x1 = None
        try:
            second_hand = landmarks[1]
            x2 = second_hand[4][1]
        except IndexError:
            x2 = None

        return x1, x2

    def make_slide_shift(self, action: str, idx: int, amount_of_slides: int):
        """Switching between one or more slides"""

        for i in range(amount_of_slides):
            pyautogui.press(action)
        self.is_slide_switched[idx] = True

        if action == "right":
            side_to_switch = "вправо"
        else:
            side_to_switch = "влево"

        text_for_log = f"{amount_of_slides} слайд(-а) {side_to_switch} с помощью {idx + 1}-ой руки"
        window.append_to_log(window.format_text_with_color(text=text_for_log, color="green"))

        self.start_count_time[idx] = None
        self.start_thumb_position[idx] = None
        self.start_gesture_time[idx] = None
        self.count_or_not[idx] = True
        self.slides_to_switch[idx] = 0
        self.ready_to_slide[idx] = False
        self.marker_to_print[idx] = 0

    def setup_units(self, img, average_length: float, cnt: int, position: str):
        """Determining values for the hand in the basic and gesture positions"""
        
        if self.hand_to_track is None:
            lm_list = self.detector.find_position(img, exact_hand="Right")
        else:
            lm_list = self.detector.find_position(img, exact_hand=self.hand_to_track)

        x = self.find_x_coordinate_of_thumbs(lm_list)[0]

        if x is not None:
            if self.start_time_to_setup_positions is None:
                self.start_time_to_setup_positions = time.time()

            length1 = self.detector.find_distance(0, 4, 8, img, draw=False)
            length2 = self.detector.find_distance(0, 4, 12, img, draw=False)
            length = length1 + length2
            is_continue = True

            if average_length != 0:
                if length > average_length * 1.2 or length < average_length - average_length * 0.2:
                    text_for_log = "Не двигайте руку! Попробуйте еще раз."
                    window.append_to_log(window.format_text_with_color(text=text_for_log, color="red"))

                    self.start_time_to_setup_positions = None
                    average_length = 0
                    cnt = 0
                    is_continue = False
                else:
                    average_length += length
                    average_length /= 2
            else:
                average_length = length

            if is_continue:
                color = "blue" if self.length_in_normal_position is None else "pink"
                dif_times = time.time() - self.start_time_to_setup_positions

                if dif_times >= 4:
                    dist = 0

                    if position == "normal":
                        self.length_in_normal_position = average_length
                        dist = self.length_in_normal_position
                    elif position == "gesture":
                        self.length_in_gesture = average_length
                        dist = self.length_in_gesture

                    self.start_time_to_setup_positions = None

                    text_for_log = f"Данные настроены."
                    window.append_to_log(window.format_text_with_color(text=text_for_log, color="green"))
                    text_for_log = f"Расстояние между пальцами: {round(dist)}"
                    window.append_to_log(window.format_text_with_color(text=text_for_log, color=color))

                    average_length = 0
                    cnt = 0
                elif dif_times >= 3:
                    if cnt == 2:
                        cnt += 1
                        window.append_to_log(window.format_text_with_color(text="1...", color=color))
                elif dif_times >= 2:
                    if cnt == 1:
                        cnt += 1
                        window.append_to_log(window.format_text_with_color(text="2...", color=color))
                elif dif_times >= 1:
                    if cnt == 0:
                        cnt += 1
                        window.append_to_log(window.format_text_with_color(text="3...", color=color))
        else:
            if self.start_time_to_setup_positions is not None:
                text_for_log = "Не убирайте руку от камеры! Попробуйте еще раз."
                window.append_to_log(window.format_text_with_color(text=text_for_log, color="red"))
                self.start_time_to_setup_positions = None
                cnt = 0
        return average_length, cnt

    def hand_tracking_function(self):
        """The main algorithm for gesture recognition and slide shifting"""

        if len(self.cameras) == 0:
            window.show_error_message("Камера не обнаружена. Подключите камеру и перезапустите приложение.")

        # Initialize the video window
        cap = cv2.VideoCapture(self.cameras[self.camera_index])
        _, image_template = cap.read()
        cv2.imshow(self.video_window_title, image_template)
        cv2.namedWindow(self.video_window_title, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.video_window_title, 400, 0)

        self.length_in_normal_position = None
        self.length_in_gesture = None
        average_length = 0
        count_to_print = 0

        text_for_log = "Поместите руку в кадр на расстоянии,"
        window.append_to_log(window.format_text_with_color(text=text_for_log, color="grey"))
        text_for_log = "на котором будет использоваться программа."
        window.append_to_log(window.format_text_with_color(text=text_for_log, color="grey"))
        text_for_log = "1. Удерживайте руку раскрытой ладонью в камеру"
        window.append_to_log(window.format_text_with_color(text=text_for_log, color="blue"))
        text_for_log = "2. Удерживайте руку в положении жеста"
        window.append_to_log(window.format_text_with_color(text=text_for_log, color="pink"))

        while self.is_video_on:
            # Capture a frame from the camera
            success, img = cap.read()
            image = cv2.flip(img, 1)  # Mirror the image
            img = self.detector.find_hands(image)

            if self.is_started and self.length_in_normal_position is None:
                average_length, count_to_print = self.setup_units(img, average_length, count_to_print,
                                                                  position="normal")

            elif self.is_started and self.length_in_gesture is None:
                average_length, count_to_print = self.setup_units(img, average_length, count_to_print,
                                                                  position="gesture")

            elif self.is_started:
                # Detect hands landmarks in the frame
                lm_list = self.detector.find_position(img, exact_hand=self.hand_to_track)

                # Find the x-coordinate of the thumbs
                x1, x2 = self.find_x_coordinate_of_thumbs(lm_list)

                for i, thumb in enumerate([x1, x2]):
                    if thumb is None:
                        continue

                    # Check the distance between the index, middle and ring fingers
                    length1 = self.detector.find_distance(i, 4, 8, img, draw=False)
                    length2 = self.detector.find_distance(i, 4, 12, img, draw=False)

                    if self.is_slide_switched.count(True) == 0:
                        if length1 + length2 <= self.length_in_gesture * 2:
                            if self.start_count_time[i] is None:
                                self.start_count_time[i] = time.time()

                            # If the initial position is not defined, set it
                            if self.start_thumb_position[i] is None:
                                self.start_thumb_position[i] = thumb

                            if self.start_gesture_time[i] is None:
                                self.start_gesture_time[i] = time.time()

                            if (time.time() - self.start_count_time[i] < self.count_time_threshold and
                                    self.count_or_not[i]):
                                self.slides_to_switch[i] += 1
                            self.count_or_not[i] = False

                            if (time.time() - self.start_gesture_time[i] > self.gesture_time_threshold and
                                    self.start_thumb_position[i] - thumb <= self.length_in_gesture and
                                    thumb - self.start_thumb_position[i] <= self.length_in_gesture):
                                self.ready_to_slide[i] = True

                                if self.marker_to_print[i] < 2:
                                    self.marker_to_print[i] += 1

                            if self.ready_to_slide[i]:
                                if self.marker_to_print[i] == 1:
                                    text_for_log = f"Готов переключить {self.slides_to_switch[i]} слайд(-а) {i + 1}-ой рукой"
                                    window.append_to_log(
                                        window.format_text_with_color(text=text_for_log, color="white"))

                                if (thumb > self.start_thumb_position[i]
                                        + self.length_in_normal_position / 4):  # If the hand moves to the right
                                    self.make_slide_shift(action="right",
                                                          idx=i,
                                                          amount_of_slides=self.slides_to_switch[i])

                                elif (thumb < self.start_thumb_position[i]
                                      - self.length_in_normal_position / 4):  # If the hand moves to the left
                                    self.make_slide_shift(action="left",
                                                          idx=i,
                                                          amount_of_slides=self.slides_to_switch[i])
                        else:
                            if self.start_count_time[i] is not None:
                                if time.time() - self.start_count_time[i] > self.count_time_threshold + 1:
                                    self.start_count_time[i] = None
                                    self.start_thumb_position[i] = None
                                    self.slides_to_switch[i] = 0

                            if self.start_thumb_position[i] is not None:
                                if (self.start_thumb_position[i] - thumb > self.length_in_gesture * 1.5 or
                                        thumb - self.start_thumb_position[i] > self.length_in_gesture * 1.5):
                                    self.start_count_time[i] = None
                                    self.start_thumb_position[i] = None
                                    self.slides_to_switch[i] = 0

                            self.start_gesture_time[i] = None
                            self.count_or_not[i] = True
                            self.ready_to_slide[i] = False
                            self.marker_to_print[i] = 0

                    elif length1 + length2 > self.length_in_normal_position / 3:
                        self.is_slide_switched[i] = False

            # Display the window
            cv2.imshow(self.video_window_title, img)
            cv2.waitKey(1)

        else:
            cap.release()
            cv2.destroyAllWindows()


def run_application():
    """Program launch"""
    try:
        window.setupUi(window)
        window.show()

        ht.hand_tracking_function()

    except Exception:
        traceback_str = traceback.format_exc()
        window.show_error_message(f"Произошла неизвестная ошибка.\n"
                                  f"Свяжитесь с исполнителем и отправьте скриншот ошибки.\n\n"
                                  f"{traceback_str}")
        sys.exit(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UiSlideShifter()
    ht = HandTracking()
    run_application()
