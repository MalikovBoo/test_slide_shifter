import cv2
import mediapipe
import math
import pyautogui
import sys

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QLabel, QPushButton, QWidget, QMessageBox, QMainWindow, QApplication)


class Ui_SlideShifter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cnt = 0
        self.is_started = False
        self.video_status = True

    def setupUi(self, SlideShifter):
        """
        Устанавливает пользовательский интерфейс для главного окна приложения.

        :param SlideShifter: Экземпляр главного окна.
        """

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

    def retranslateUi(self, SlideShifter):
        """
        Переводит названия элементов интерфейса на заданный язык.

        :param SlideShifter: Экземпляр главного окна.
        """

        SlideShifter.setWindowTitle(QCoreApplication.translate("SlideShifter", u"SlideShifterVideo", None))
        self.start_button.setText(QCoreApplication.translate("SlideShifter", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.stop_button.setText(QCoreApplication.translate("SlideShifter", u"\u0421\u0442\u043e\u043f", None))
        self.label.setText(QCoreApplication.translate("SlideShifter", u"Slide Shifter", None))
        self.turn_on_off_button.setText(QCoreApplication.translate("SlideShifter",
                                                                   u"\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u044c/\u0412\u044b\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0432\u0438\u0434\u0435\u043e",
                                                                   None))

    def do_actions(self):
        """
        Назначает обработчики событий для кнопок в пользовательском интерфейсе.
        """

        self.start_button.clicked.connect(self.start_hand_tracking)
        self.stop_button.clicked.connect(self.stop_hand_tracking)
        self.turn_on_off_button.clicked.connect(self.turn_on_off_video)

    def start_hand_tracking(self):
        """
        Запускает отслеживание руки.
        """

        self.is_started = True
        ht.is_started = self.is_started
        ht.hand_tracking_function()

    def stop_hand_tracking(self):
        """
        Останавливает отслеживание руки.
        """

        self.is_started = False
        ht.is_started = False
        ht.hand_tracking_function()

    def turn_on_off_video(self):
        """
        Включает или выключает видеопоток.
        """

        self.cnt += 1
        if self.cnt % 2 == 0:
            self.video_status = True
        else:
            self.video_status = False

        ht.video_on = self.video_status
        ht.hand_tracking_function()

    def closeEvent(self, event):
        """
        Обрабатывает событие закрытия главного окна.

        :param event: Событие закрытия окна.
        """

        reply = self.show_quit_confirmation_dialog()
        if reply == QMessageBox.Yes:
            event.accept()
            exit(0)
        else:
            event.ignore()

    def show_quit_confirmation_dialog(self):
        """
        Отображает диалоговое окно с подтверждением закрытия приложения.

        :return: Ответ пользователя на вопрос о закрытии приложения.
        """

        exit_answer = QMessageBox.question(self, "Подтверждение закрытия",
                                           "Вы уверены, что хотите закрыть приложение?",
                                           QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        return exit_answer


class HandDetector:
    """
    Класс HandDetector использует библиотеку Mediapipe для обнаружения и отслеживания рук в видеопотоке.
    """

    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_con=0.5, track_con=0.5):
        """
        Инициализирует объект HandDetector с параметрами.

        :param mode: Режим работы детектора рук (по умолчанию False).
        :param max_hands: Максимальное количество рук для отслеживания (по умолчанию 2).
        :param model_complexity: Сложность модели детектора рук (по умолчанию 1).
        :param detection_con: Порог обнаружения руки (по умолчанию 0.5).
        :param track_con: Порог отслеживания руки (по умолчанию 0.5).
        """
        self.lm_list = []  # Список для хранения координат ключевых точек руки
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
        Находит и отображает руки на изображении.

        :param image: Исходное изображение.
        :param draw: Флаг отрисовки результатов (по умолчанию True).
        :return: Изображение с отрисованными руками.
        """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return image

    def find_position(self, image, hand_no=0, draw=True):
        """
        Находит позицию ключевых точек (landmarks) и ограничивающий прямоугольник вокруг руки.

        :param image: Исходное изображение.
        :param hand_no: Индекс руки в случае, если обнаружено более одной (по умолчанию 0).
        :param draw: Флаг отрисовки результатов (по умолчанию True).
        :return: Список координат ключевых точек и координаты ограничивающего прямоугольника.
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
        Находит расстояние между двумя точками на изображении и отрисовывает результат, если флаг draw установлен в True.

        :param index1: Индекс первой точки в списке ключевых точек.
        :param index2: Индекс второй точки в списке ключевых точек.
        :param image: Исходное изображение.
        :param draw: Флаг отрисовки результатов (по умолчанию True).
        :return: Расстояние между точками, изображение с отрисованными элементами и координаты точек и их центра.
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


class HandTracking():
    def __init__(self):
        self.video_window_title = "SlideShifterVideo"
        self.start_thumb_position = None
        self.slide_not_switched = True
        self.video_on = True
        self.is_started = False

    def hand_tracking_function(self):
        cap = cv2.VideoCapture(0)
        # Инициализация видеокамеры
        cv2.namedWindow(self.video_window_title, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.video_window_title, 400, 0)

        # Инициализация детектора руки
        detector = HandDetector(detection_con=0.8)

        while self.video_on:
            # Захват кадра с камеры
            success, img = cap.read()
            image = cv2.flip(img, 1)
            img = detector.find_hands(image)

            if self.is_started:
                # Обнаружение руки на кадре
                lm_list, _ = detector.find_position(img)

                if len(lm_list) != 0:
                    # Находим координаты x большого пальца
                    x = lm_list[4][1]

                    # Проверяем расстояние между указательным и средним пальцем
                    length1, _, _ = detector.find_distance(4, 8, img, draw=False)
                    length2, _, _ = detector.find_distance(4, 12, img, draw=False)

                    if self.slide_not_switched:
                        if length1 + length2 <= 120:
                            # Если начальное положение не определено, устанавливаем его
                            if self.start_thumb_position is None:
                                self.start_thumb_position = x

                            if x > self.start_thumb_position + 90:  # Если рука двигается вправо
                                print("Left slide")
                                pyautogui.press("left")
                                self.start_thumb_position = None
                                self.slide_not_switched = False

                            elif x < self.start_thumb_position - 90:  # Если рука двигается влево
                                print("Right slide")
                                pyautogui.press("right")
                                self.start_thumb_position = None
                                self.slide_not_switched = False

                    elif length1 + length2 > 120:
                        self.slide_not_switched = True

            # Отображение окна
            frame_re = cv2.resize(img, (1024, 576))
            cv2.imshow(self.video_window_title, frame_re)

            cv2.waitKey(1)

        if not self.video_on:
            cap.release()
            cv2.destroyAllWindows()


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
