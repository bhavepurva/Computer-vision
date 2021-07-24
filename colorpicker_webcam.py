import cv2
import numpy as np

def empty():
    pass

cap=cv2.VideoCapture(0)
cap.set(3,500)
cap.set(4,500)

cv2.namedWindow("trackbar")
cv2.resizeWindow("trackbar", 500, 300)

cv2.createTrackbar("hue min", "trackbar", 0, 179, empty)
cv2.createTrackbar("hue max", "trackbar", 179, 179, empty)
cv2.createTrackbar("sat min", "trackbar", 0, 255, empty)
cv2.createTrackbar("sat max", "trackbar", 255, 255, empty)
cv2.createTrackbar("val min", "trackbar", 0, 255, empty)
cv2.createTrackbar("val max", "trackbar", 255, 255, empty)

while True:
    success,img=cap.read()

    imghsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("hue min", "trackbar")
    h_max = cv2.getTrackbarPos("hue max", "trackbar")
    s_min = cv2.getTrackbarPos("sat min", "trackbar")
    s_max = cv2.getTrackbarPos("sat max", "trackbar")
    v_min = cv2.getTrackbarPos("val min", "trackbar")
    v_max = cv2.getTrackbarPos("val max", "trackbar")

    print(h_min, h_max, s_min, s_max, v_min, v_max)

    # creating mask, filteer out image of color we want
    lower, upper = np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imghsv, lower, upper)
    cv2.imshow("Video",img)
    cv2.imshow("mask",mask)

    # cv2.imshow("hsv",imghsv)
    if cv2.waitKey(1)  & 0xFF==ord("q"):
        break