# viola and jones realtime face detection
# get the image, convert to grayscale, get face cascade, detect multi-scale, apply rectangle
import cv2

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# img=cv2.imread("lena.jpg")
# imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# faces=faceCascade.detectMultiScale(imgGray,1.1,4)
# for (x,y,w,h) in faces:
#     cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)

# cv2.imshow("Image",img)
# cv2.waitKey(0)


#face detection in webcam
cap = cv2.VideoCapture(0)
cap.set(3, 500)
cap.set(4, 500)

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
