import cv2
import numpy as np

def empty(a):
    pass

# to get real time we use trackbar to obtain max and min vals of our color
# creating new window for trackbar,name has to be same
cv2.namedWindow("trackbar")
cv2.resizeWindow("trackbar", 500, 300)

cv2.createTrackbar("hue min", "trackbar", 0, 179, empty)
cv2.createTrackbar("hue max", "trackbar", 179, 179, empty)
cv2.createTrackbar("sat min", "trackbar", 64, 255, empty)
cv2.createTrackbar("sat max", "trackbar", 216, 255, empty)
cv2.createTrackbar("val min", "trackbar", 28, 255, empty)
cv2.createTrackbar("val max", "trackbar", 255, 255, empty)

while True:
    img = cv2.imread("money_heist.jpg")
    img = cv2.resize(img, (250, 250))

    # convert image to hsv, hue saturation value
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("hue min", "trackbar")
    h_max = cv2.getTrackbarPos("hue max", "trackbar")
    s_min = cv2.getTrackbarPos("sat min", "trackbar")
    s_max = cv2.getTrackbarPos("sat max", "trackbar")
    v_min = cv2.getTrackbarPos("val min", "trackbar")
    v_max = cv2.getTrackbarPos("val max", "trackbar")

    print(h_min,h_max,s_min,s_max,v_min,v_max)

    #creating mask, filteer out image of color we want
    lower,upper=np.array([h_min,s_min,v_min]),np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHsv,lower,upper)

    #get actual color over mask
    result=cv2.bitwise_and(img,img,mask=mask)

    # cv2.imshow("image", img)
    # cv2.imshow("hsv image", imgHsv)
    cv2.imshow("mask image", mask)
    # cv2.imshow("result image", result)
    hor=np.hstack((img,imgHsv,result))
    cv2.imshow("stack", hor)

    cv2.waitKey(1) #1 is important
