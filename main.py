import cv2
import hand_tracking as htm
import pyautogui

is_started = False


def start_hand_tracking():
    # Инициализация видеокамеры
    cap = cv2.VideoCapture(0)
    cap.set(3, 150)
    cap.set(4, 200)

    # Инициализация детектора руки
    detector = htm.HandDetector(detection_con=0.8)

    # Начальное положение большого пальца на ладони
    start_x = None

    # Флаг активации переключения слайдов
    slide_not_switched = True

    while True:
        # Захват кадра с камеры
        success, img = cap.read()
        image = cv2.flip(img, 1)
        img = detector.find_hands(image)

        if is_started:
            # Обнаружение руки на кадре
            lm_list, _ = detector.find_position(img)

            if len(lm_list) != 0:
                # Находим координаты x большого пальца
                x = lm_list[4][1]

                # Проверяем расстояние между указательным и средним пальцем
                length_1, _, _ = detector.find_distance(4, 8, img, draw=False)
                length_2, _, _ = detector.find_distance(4, 12, img, draw=False)

                if slide_not_switched:
                    if length_1 + length_2 <= 130:
                        # Если начальное положение не определено, устанавливаем его
                        if start_x is None:
                            start_x = x

                        # print("ready to slide")

                        if x > start_x + 90:  # Если рука двигается вправо
                            print("Left slide")
                            pyautogui.press('left')
                            start_x = None  # Обновляем начальное положение
                            slide_not_switched = False

                        elif x < start_x - 90:  # Если рука двигается влево
                            print("Right slide")
                            pyautogui.press('right')
                            start_x = None  # Обновляем начальное положение
                            slide_not_switched = False

                elif length_1 + length_2 > 120:
                    slide_not_switched = True
                # print(slide_not_switched)

        # Отображение окна
        cv2.imshow("SlideShifterVideo", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    start_hand_tracking()
