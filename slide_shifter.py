import cv2
import mediapipe
import math
import pyautogui
import sys
from enum import Enum
from PySide6.QtCore import QMetaObject, QRect
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QMessageBox, QMainWindow, QApplication)


class ButtonColors(Enum):
    START = "rgb(107, 182, 84)"
    STOP = "rgb(189, 54, 43)"
    TURN_ON_OFF = "rgb(52, 120, 246)"


class Ui_SlideShifter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cnt = 0
        self.is_started = False
        self.video_status = True

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
        self.set_button_style(self.start_button, ButtonColors.START)

        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(30, 370, 340, 150))
        self.set_button_style(self.stop_button, ButtonColors.STOP)

        self.turn_on_off_button = QPushButton(self.centralwidget)
        self.turn_on_off_button.setObjectName(u"turn_on_off_button")
        self.turn_on_off_button.setGeometry(QRect(30, 530, 340, 70))
        self.set_button_style(self.turn_on_off_button, ButtonColors.TURN_ON_OFF)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 60, 240, 50))
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 900 28pt \"Futura\";")

        SlideShifter.setCentralWidget(self.centralwidget)
        self.setText(SlideShifter)

        QMetaObject.connectSlotsByName(SlideShifter)
        self.do_actions()

    def set_button_style(self, button, color):
        # Set the style for the buttons
        button.setStyleSheet(f"background-color: {color.value};\n"
                             "font: 300 24pt \"Helvetica Neue\";\n"
                             "color: rgb(0, 0, 0);")

    def setText(self, SlideShifter):
        # Set text for labels and buttons
        SlideShifter.setWindowTitle("Slide Shifter")
        self.start_button.setText("Start")
        self.stop_button.setText("Stop")
        self.label.setText("Slide Shifter")
        self.turn_on_off_button.setText("Pause")

    def do_actions(self):
        # Connect button clicks to corresponding functions
        self.start_button.clicked.connect(self.start_hand_tracking)
        self.stop_button.clicked.connect(self.stop_hand_tracking)
        self.turn_on_off_button.clicked.connect(self.pause_video)

    def start_hand_tracking(self):
        # Start hand tracking function
        self.is_started = True
        ht.is_started = self.is_started
        ht.hand_tracking_function()

    def stop_hand_tracking(self):
        # Stop hand tracking function
        self.is_started = False
        ht.is_started = False
        ht.hand_tracking_function()

    def pause_video(self):
        # Pause/unpause video
        self.cnt += 1
        self.video_status = self.cnt % 2 == 0
        ht.video_on = self.video_status
        ht.hand_tracking_function()

    def closeEvent(self, event):
        # Handle close event for the main window
        reply = self.show_quit_confirmation_dialog()
        if reply == QMessageBox.Yes:
            event.accept()
            ht.cap.release()
            cv2.destroyAllWindows()
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
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detection_con=0.8)

    def hand_tracking_function(self):
        """
        Performs hand tracking using the initialized video capture and hand detector.

        It initializes the video window, captures frames from the camera, detects hands, and controls the slide based on hand movements.
        """
        # Initialize the video window
        cv2.namedWindow(self.video_window_title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.video_window_title, 800, 600)
        cv2.moveWindow(self.video_window_title, 400, 0)

        while self.video_on:
            # Capture a frame from the camera
            success, img = self.cap.read()
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
                            # If the initial position is not defined, set it
                            if self.start_thumb_position is None:
                                self.start_thumb_position = x

                            if x > self.start_thumb_position + 90:  # If the hand moves to the right
                                print("Left slide")
                                pyautogui.press("left")
                                self.start_thumb_position = None
                                self.slide_not_switched = False

                            elif x < self.start_thumb_position - 90:  # If the hand moves to the left
                                print("Right slide")
                                pyautogui.press("right")
                                self.start_thumb_position = None
                                self.slide_not_switched = False

                    elif length1 + length2 > 120:
                        self.slide_not_switched = True

            # Display the window
            cv2.imshow(self.video_window_title, img)

            cv2.waitKey(1)


def run_application():
    app = QApplication(sys.argv)
    window = Ui_SlideShifter()
    ui = Ui_SlideShifter()
    ui.setupUi(window)
    window.show()

    ht.hand_tracking_function()

    sys.exit(app.exec())


if __name__ == "__main__":
    ht = HandTracking()
    run_application()
