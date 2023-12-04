import cv2
import mediapipe as mp
import time
import math


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

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_con,
                                         self.track_con)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        """
        Находит и отображает руки на изображении.

        :param img: Исходное изображение.
        :param draw: Флаг отрисовки результатов (по умолчанию True).
        :return: Изображение с отрисованными руками.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        """
        Находит позицию ключевых точек (landmarks) и ограничивающий прямоугольник вокруг руки.

        :param img: Исходное изображение.
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
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)
        return self.lm_list, bbox

    def find_distance(self, p1, p2, img, draw=True):
        """
        Находит расстояние между двумя точками на изображении и отрисовывает результат, если флаг draw установлен в True.

        :param p1: Индекс первой точки в списке ключевых точек.
        :param p2: Индекс второй точки в списке ключевых точек.
        :param img: Исходное изображение.
        :param draw: Флаг отрисовки результатов (по умолчанию True).
        :return: Расстояние между точками, изображение с отрисованными элементами и координаты точек и их центра.
        """
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    """
    Основная функция программы для обработки видеопотока с веб-камеры и отображения руки с дополнительной информацией.

    :return: None
    """
    p_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        if len(lm_list) != 0:
            print(lm_list[1])

        c_time = time.time()
        fps = 1. / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Test Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
