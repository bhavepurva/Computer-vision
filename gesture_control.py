import cv2, time
import mediapipe as mp
import numpy as np
import math
import hand_tracking as ht

detector = ht.hand_tracker(tracking_confidence=0.7)
cam_width, cam_height = 500, 500

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)
current_time = 0
prev_time = 0

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=False)
    if len(lm_list) != 0:
        # print(lm_list[8])

        x1,y1=lm_list[4][1],lm_list[4][2]
        x2,y2=lm_list[8][1],lm_list[8][2]

        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)

        # dist=math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
        # if dist<=10:
        #     print("do something")
        length=math.hypot(x2-x1,y2-y1)
        if length<30:
            cv2.circle(img,(cx,cy),10,(255,255,255),cv2.FILLED)
            img=cv2.resize(img,(200,200))
        elif length>200:
            cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
            img = cv2.resize(img, (800, 800))
        # if length:
        #     img=cv2.resize(img,(int(length*10),int(length*10)))


    # current_time = time.time()
    # fps = 1 / (current_time - prev_time)
    # prev_time = current_time
    # cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 5)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
