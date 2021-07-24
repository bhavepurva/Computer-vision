import cv2
import numpy as np

img=cv2.imread("money_heist.jpg")
img=cv2.resize(img,(300,300))

#we need kernel matrix for dialation, we generate it using numpy
kernel=np.ones((5,5),np.uint8)

#cvt color used to change img to diff color space
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#ksize is amount of blurness 7,7 has to be odd number,sigmax is 0
imgBlur=cv2.GaussianBlur(imgGray,(7,7),0)


#canny image to detect edge,200 is threshold vals
imgCanny=cv2.Canny(img,200,200)

#to increase thickness of edge in canny image
#increasing iteration increases the thickness of edges
imgDial=cv2.dilate(imgCanny,kernel,iterations=1)

#erosion makes edges thinner
imgErr=cv2.erode(imgDial,kernel,iterations=1)

#display image
cv2.imshow("Gray Image",imgGray)
cv2.imshow("Blur Image",imgBlur)
cv2.imshow("Canny Image",imgCanny)
cv2.imshow("Dilated Image",imgDial)
cv2.imshow("Erroded Image",imgErr)


cv2.waitKey(0)

