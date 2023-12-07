import cv2
import hand_tracking as htm
import pyautogui

is_started = False
video_on = True


def hand_tracking_function():
    # Инициализация видеокамеры
    cap = cv2.VideoCapture(0)

    # Инициализация детектора руки
    detector = htm.HandDetector(detection_con=0.8)

    # Начальное положение большого пальца на ладони
    start_x = None

    # Флаг активации переключения слайдов
    slide_not_switched = True

    while video_on:
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

        # Отображение окна, только если video_on равно True
        frame_re = cv2.resize(img, (1024, 576))
        cv2.imshow("SlideShifterVideo", frame_re)

        cv2.waitKey(1)

    # Закрыть видео, если video_on = False
    if not video_on:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    hand_tracking_function()
