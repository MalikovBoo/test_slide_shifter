import cv2
import mediapipe
import math
import pyautogui
import sys
import time

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
                               QPushButton, QWidget, QMessageBox)


class UiSlideShifter(QMainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, SlideShifter):
        if not SlideShifter.objectName():
            SlideShifter.setObjectName(u"SlideShifter")
        SlideShifter.move(0, 0)
        SlideShifter.resize(400, 720)
        SlideShifter.setStyleSheet(u"background-color: rgb(40, 40, 40);\n"
                                   "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.497014, radius:0.485181, fx:0.496641, fy:0.443, stop:0 rgba(38, 90, 222, 255), stop:0.16 rgba(150, 161, 228, 255), stop:0.225 rgba(140, 163, 244, 255), stop:0.285 rgba(202, 189, 247, 255), stop:0.345 rgba(153, 172, 255, 255), stop:0.415 rgba(208, 187, 231, 255), stop:0.52 rgba(123, 118, 228, 255), stop:0.57 rgba(98, 128, 208, 255), stop:0.635 rgba(121, 139, 200, 255), stop:0.695 rgba(137, 146, 201, 255), stop:0.75 rgba(129, 151, 216, 255), stop:0.815 rgba(154, 164, 208, 255), stop:0.88 rgba(137, 148, 205, 255), stop:0.935 rgba(216, 217, 224, 255), stop:1 rgba(255, 255, 255, 255));")
        self.centralwidget = QWidget(SlideShifter)
        self.centralwidget.setObjectName(u"centralwidget")
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(50, 250, 300, 150))
        self.start_button.setStyleSheet(u"background-color: rgb(128, 185, 116);\n"
                                        "font: 400 24pt \"Helvetica Neue\";\n"
                                        "color: rgb(0, 0, 0);")
        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(50, 420, 300, 150))
        self.stop_button.setStyleSheet(u"background-color: rgb(234, 77, 62);\n"
                                       "color: rgb(0, 0, 0);\n"
                                       "font: 400 24pt \"Helvetica Neue\";")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(102, 100, 195, 39))
        font = QFont()
        font.setFamilies([u"Futura"])
        font.setPointSize(30)
        font.setWeight(QFont.Black)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                 "color: rgb(24, 24, 24);\n"
                                 "font: 900 30pt \"Futura\";")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(132, 680, 136, 20))
        font1 = QFont()
        font1.setFamilies([u"Futura"])
        font1.setPointSize(16)
        font1.setWeight(QFont.DemiBold)
        font1.setItalic(False)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                   "color: rgb(84, 85, 85);\n"
                                   "font: 600 16pt \"Futura\";\n"
                                   "")
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(310, 20, 80, 21))
        self.comboBox.setStyleSheet(u"color: rgb(0, 0, 0);\n"
                                    "background-color: rgb(151, 152, 152);\n"
                                    "font: 300 14pt \"Helvetica Neue\";")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(240, 20, 61, 19))
        self.label_3.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                   "color: rgb(32, 32, 32);\n"
                                   "font: 400 16pt \"Helvetica Neue\";\n"
                                   "")
        SlideShifter.setCentralWidget(self.centralwidget)
        self.get_connected_cameras()
        self.comboBox.activated.connect(self.activated)
        self.retranslateUi(SlideShifter)

        QMetaObject.connectSlotsByName(SlideShifter)
        self.connect_buttons()

    def retranslateUi(self, SlideShifter):
        SlideShifter.setWindowTitle(QCoreApplication.translate("SlideShifter", u"Slide Shifter", None))
        self.start_button.setText(
            QCoreApplication.translate("SlideShifter", u"\u041d\u0430\u0447\u0430\u0442\u044c", None))
        self.stop_button.setText(QCoreApplication.translate("SlideShifter",
                                                            u"\u041f\u0440\u0438\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c ",
                                                            None))
        self.label.setText(QCoreApplication.translate("SlideShifter", u"Slide Shifter", None))
        self.label_2.setText(QCoreApplication.translate("SlideShifter", u"by Singularity Hub", None))

        self.label_3.setText(QCoreApplication.translate("SlideShifter", u"Camera:", None))

    def connect_buttons(self):
        # Connect button clicks to corresponding functions
        self.start_button.clicked.connect(self.start_hand_tracking)
        self.stop_button.clicked.connect(self.stop_hand_tracking)

    def get_connected_cameras(self):
        cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if not cap.isOpened():
                break
            cameras.append(i)
            cap.release()
            self.comboBox.addItem("")
            self.comboBox.setItemText(i, QCoreApplication.translate("SlideShifter", f"№{i + 1}", None))
        ht.cameras = cameras

    def activated(self, index):
        ht.camera_index = index
        ht.hand_tracking_function()

    def start_hand_tracking(self):
        # Start hand tracking function
        ht.is_started = True
        print("started")
        ht.hand_tracking_function()

    def stop_hand_tracking(self):
        # Stop hand tracking function
        ht.is_started = False
        print("paused")
        ht.hand_tracking_function()

    def closeEvent(self, event):
        # Handle close event for the main window
        reply = self.show_quit_confirmation_dialog()
        if reply == QMessageBox.Yes:
            event.accept()
            ht.video_on = False
            ht.hand_tracking_function()
            sys.exit(0)
        else:
            event.ignore()

    def show_quit_confirmation_dialog(self):
        # Show quit confirmation dialog
        exit_answer = QMessageBox.question(self, "Подтверждение закрытия",
                                           "Вы уверены, что хотите закрыть приложение?",
                                           QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        return exit_answer


class HandDetector:
    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_con=0.5, track_con=0.5):
        """
        Initializes an instance of the HandDetector class with specified parameters.

        :param mode: Hand detector mode (default is False).
        :param max_hands: Maximum number of hands to track (default is 2).
        :param model_complexity: Model complexity of the hand detector (default is 1).
        :param detection_con: Detection confidence threshold for hand detection (default is 0.5).
        :param track_con: Tracking confidence threshold for hand tracking (default is 0.5).
        """
        self.lm_list = []  # List to store coordinates of hand landmarks
        self.results = None
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mediapipe.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_con,
                                         self.track_con)
        self.mp_draw = mediapipe.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, image, draw=True):
        """
        Finds and visualizes hands on the image.

        :param image: Source image.
        :param draw: Flag for drawing the results (default is True).
        :return: Image with annotated hands.
        """
        if image is None:
            return None
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return image

    def find_position(self, image, hand_no=0, draw=True):
        """
        Finds the position of hand landmarks and the bounding rectangle around the hand.

        :param image: Source image.
        :param hand_no: Index of the hand in case of multiple hands (default is 0).
        :param draw: Flag for drawing the results (default is True).
        :return: List of coordinates of hand landmarks and coordinates of the bounding rectangle.
        """
        x_list = []
        y_list = []
        bbox = []
        self.lm_list = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(image, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)
        return self.lm_list, bbox

    def find_distance(self, index1, index2, image, draw=True):
        """
        Finds the distance between two points on the image and visualizes the result if the draw flag is set to True.
        :param index1: Index of the first point in the list of hand landmarks.
        :param index2: Index of the second point in the list of hand landmarks.
        :param image: Source image.
        :param draw: Flag for drawing the results (default is True).
        :return: Distance between the points, image with annotated elements, and coordinates of the points and their center.
        """
        x1, y1 = self.lm_list[index1][1], self.lm_list[index1][2]
        x2, y2 = self.lm_list[index2][1], self.lm_list[index2][2]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if draw:
            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, image, [x1, y1, x2, y2, cx, cy]


class HandTracking:
    def __init__(self):
        """
        Initializes an instance of the HandTracking class.

        Attributes:
            video_window_title (str): Title of the video window.
            start_thumb_position (int or None): Initial position of the thumb.
            slide_not_switched (bool): Flag indicating whether the slide is not switched.
            video_on (bool): Flag indicating whether the video is on.
            is_started (bool): Flag indicating whether hand tracking is started.
            cap (cv2.VideoCapture): Video capture object.
            detector (HandDetector): Instance of the HandDetector class for hand tracking.
        """
        self.video_window_title = "Slide Shifter Video"
        self.start_thumb_position = None
        self.slide_not_switched = True
        self.video_on = True
        self.is_started = False
        self.cameras = [0, ]
        self.camera_index = 0
        self.detector = HandDetector(detection_con=0.8)

    def hand_tracking_function(self):
        """
        Performs hand tracking using the initialized video capture and hand detector.

        It initializes the video window, captures frames from the camera, detects hands, and controls the slide based on hand movements.
        """
        # Initialize the video window
        cap = cv2.VideoCapture(self.cameras[self.camera_index])

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
        __, _ = cap.read()
        cv2.imshow(self.video_window_title, _)
        cv2.namedWindow(self.video_window_title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.video_window_title, width, height)
        cv2.moveWindow(self.video_window_title, 400, 0)

        start_gesture_time = None
        gesture_time_threshold = 0.2
        ready_to_slide = False

        while self.video_on:
            # Capture a frame from the camera
            success, img = cap.read()
            image = cv2.flip(img, 1)
            img = self.detector.find_hands(image)

            if self.is_started:
                # Detect hand landmarks in the frame
                lm_list, _ = self.detector.find_position(img)

                if len(lm_list) != 0:
                    # Find the x-coordinate of the thumb
                    x = lm_list[4][1]

                    # Check the distance between the index and middle fingers
                    length1, _, _ = self.detector.find_distance(4, 8, img, draw=False)
                    length2, _, _ = self.detector.find_distance(4, 12, img, draw=False)

                    if self.slide_not_switched:
                        if length1 + length2 <= 120:
                            if start_gesture_time is None:
                                start_gesture_time = time.time()

                            # If the initial position is not defined, set it
                            if self.start_thumb_position is None:
                                self.start_thumb_position = x

                            if (time.time() - start_gesture_time > gesture_time_threshold and
                                    self.start_thumb_position - x <= 50 and
                                    x - self.start_thumb_position <= 50 and
                                    length1 + length2 <= 100):
                                ready_to_slide = True
                                print("ready to slide")

                            if ready_to_slide:
                                if x > self.start_thumb_position + 120:  # If the hand moves to the right
                                    print("Right slide")
                                    pyautogui.press("right")
                                    self.start_thumb_position = None
                                    start_gesture_time = None
                                    self.slide_not_switched = False
                                    ready_to_slide = False

                                elif x < self.start_thumb_position - 110:  # If the hand moves to the left
                                    print("Left slide")
                                    pyautogui.press("left")
                                    self.start_thumb_position = None
                                    start_gesture_time = None
                                    self.slide_not_switched = False
                                    ready_to_slide = False

                        elif start_gesture_time is not None:
                            start_gesture_time = None
                            self.start_thumb_position = None
                            ready_to_slide = False
                            print("failed slide")

                    elif length1 + length2 > 120:
                        self.slide_not_switched = True

            # Display the window
            cv2.imshow(self.video_window_title, img)

            cv2.waitKey(1)
        else:
            cap.release()
            cv2.destroyAllWindows()


def run_application():
    app = QApplication(sys.argv)
    window = UiSlideShifter()
    window.setupUi(window)
    window.show()

    ht.hand_tracking_function()

    sys.exit(app.exec())


if __name__ == "__main__":
    ht = HandTracking()
    run_application()
