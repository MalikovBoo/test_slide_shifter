
import cv2
import HandTrackingModule as htm
import pyautogui

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.8)
startX = None
# Начальное положение центра ладони
cx, cy = 0, 0
# Флаг активации переключения слайдов
slide_switch_active = False
slide_not_switched = True

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if len(lmList) != 0:
        # Находим координаты x большого пальца
        x = lmList[4][1]

        # Проверяем расстояние между указательным и средним пальцем
        length_1, _, _ = detector.findDistance(4, 8, img, draw=False)
        length_2, _, _ = detector.findDistance(4, 12, img, draw=False)

        if slide_not_switched:
            if length_1 + length_2 <= 130:
                # Если начальное положение не определено, устанавливаем его
                if startX is None:
                    startX = x

                print("ready to slide")

                if x > startX + 90:  # Если рука двигается вправо
                    print("left slide")
                    pyautogui.press('left')
                    startX = None  # Обновляем начальное положение
                    slide_not_switched = False

                elif x < startX - 90:  # Если рука двигается влево
                    print("right slide")
                    pyautogui.press('right')
                    startX = None  # Обновляем начальное положение
                    slide_not_switched = False

        elif length_1 + length_2 > 120:
            slide_not_switched = True
        print(slide_not_switched)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


