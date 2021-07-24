import cv2

# to read image
img = cv2.imread("money_heist.jpg")

# actual size of image
print(img.shape)  # 630,630,3 height,width,color(rgb)

# to resize the image
resized_img = cv2.resize(img, (300, 300))

#to crop images, lis takes height first then width
cropped_img=img[0:300,200:500 ]

# to display image
cv2.imshow("Image", img)
cv2.imshow("Resized Image", resized_img)
cv2.imshow("Cropped Image", cropped_img)

# to add delay, 0 is infinite, delay in ms
cv2.waitKey(0)

# to capture video
# cap=cv2.VideoCapture("vid.mp4")

# to use webcam
# cap=cv2.VideoCapture(0) #zero value means use the default webcam

# to change size of window
# cap.set(3,500) #width
# cap.set(4,480) #height
# # cap.set(10,n) for brightness
#
# while True:
#     success,img=cap.read()
#     cv2.imshow("Video",img)
#     #increase waitkey to make video slow
#     if cv2.waitKey(25) & 0xFF==ord("q"):
#         break
#
# cap.release()



