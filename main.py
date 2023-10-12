
import cv2
import HandTrackingModule as htm
import pyautogui

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.8)

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
        # Находим координаты центра ладони (можно использовать другую точку, если нужно)
        x, y = lmList[9][1], lmList[9][2]

        # Проверяем расстояние между указательным и средним пальцем
        length_next, _, _ = detector.findDistance(4, 8, img, draw=False)
        length_prev, _, _ = detector.findDistance(4, 12, img, draw=False)


        if slide_not_switched:
            if length_next <= 70:
                pyautogui.press('right')
                slide_not_switched = False
            elif length_prev <= 70:
                pyautogui.press('left')
                slide_not_switched = False
        elif length_next > 70 and length_prev > 70:
            slide_not_switched = True
        print(slide_not_switched)


    cv2.imshow("Image", img)
    cv2.waitKey(1)


