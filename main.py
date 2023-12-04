import cv2
import HandTrackingModule as htm
import pyautogui

# Инициализация видеокамеры
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Инициализация детектора руки
detector = htm.HandDetector(detection_con=0.8)

# Начальное положение большого пальца на ладони
start_x = None

# Начальное положение центра ладони
cx, cy = 0, 0

# Флаг активации переключения слайдов
slide_switch_active = False
slide_not_switched = True

while True:
    # Захват кадра с камеры
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Обнаружение руки на кадре
    img = detector.find_hands(img)
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

    # Отображение окна с названием "Slide Shifter"
    cv2.imshow("Slide Shifter", img)
    cv2.waitKey(1)
