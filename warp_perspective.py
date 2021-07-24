import cv2
import numpy as np

# get birdeye view, get skew image as flat as possible
img = cv2.imread("warp.jpg")
width, height = 100, 200

# get corner points ofour image
points = np.float32([[26, 113], [95, 105], [110, 203], [28, 215]])
points2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

matrix = cv2.getPerspectiveTransform(points, points2)
imgWarp = cv2.warpPerspective(img, matrix, (100, 200))

cv2.imshow("Image", img)
cv2.imshow("Warp", imgWarp)

cv2.waitKey(0)


