import cv2
import numpy as np


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cont in contours:
        area = cv2.contourArea(cont)
        print(area)
        # third argument is index of contours, to draw all contours put -1
        cv2.drawContours(imgContour, cont, -1, (255, 0, 0), 1)
        # draw contour -> original image, contours obtained, index of countours, color and lastly thickness
        peri = cv2.arcLength(cont, True)
        print(peri)
        approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
        print(len(approx))
        objCorner = len(approx)
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # rectangle -> original image, start point, endpoint, color ,thickness
        if objCorner == 3:
            objType = "triangle"
        elif objCorner == 4:
            objType = "rectangle"
        elif objCorner > 5:
            objType = "circle"
        else:
            objType = "None"

        cv2.putText(imgContour, objType, (x + w // 2 - 10, y + h // 2 - 10), cv2.FONT_ITALIC, 0.5, (0, 0, 255), 2)


# convert to grayscale to get edges and thus find corner points
img = cv2.imread("shapes.png")
imgContour = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)

# to detect edges
imgCanny = cv2.Canny(imgGray, 50, 50)
getContours(imgCanny)

# cv2.imshow("Image",img)
cv2.imshow("Contoured Image", imgContour)

# cv2.imshow("Gray Image",imgGray)
# cv2.imshow("Blur Image",imgBlur)
hor = np.hstack((imgGray, imgBlur, imgCanny))

cv2.imshow("Images", hor)
cv2.waitKey(0)
