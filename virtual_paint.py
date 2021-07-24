import cv2,time
import mediapipe as mp
import hand_tracking as ht
import numpy as np

cam_width,cam_height=500,500

detector=ht.hand_tracker(detection_confidence=0.85)

cap=cv2.VideoCapture(0)
cap.set(3,cam_width)
cap.set(4,cam_height)

paint_colors=(255,255,255)

img_canvas=np.zeros((480,640,3),np.uint8)

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)

    img=detector.find_hands(img)
    lm_list=detector.find_position(img,draw=False)

    if len(lm_list)!=0:
        #index finger


        x1,y1=lm_list[8][1],lm_list[8][2]

        #middle finger
        x2, y2 = lm_list[12][1], lm_list[12][2]

        fingers=detector.fingers_that_are_up()
        # print(fingers)

        if fingers[1] and fingers[2]:
            # print("selection")
            xp, yp = 0, 0
            if y1<100:
                if 0<x1<130:
                    paint_colors = (255, 255, 255)  #white
                elif 130<x1<260:
                    paint_colors=(0,0,255)  #red
                elif 260<x1<390:
                    paint_colors=(0,255,0)  #green
                elif 390<x1<520:
                    paint_colors=(255,0,0)  #blue
                elif 520<x1<650:
                    paint_colors=(0,0,0)  #eraser


            cv2.circle(img, (x1, y1), 10, paint_colors, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, paint_colors, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), paint_colors, 2)



        if fingers[1] and fingers[2]==False:
            # print("drawing")
            cv2.circle(img,(x1,y1),10,paint_colors,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if paint_colors==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), paint_colors, 70)
                cv2.line(img_canvas, (xp, yp), (x1, y1), paint_colors, 70)

            cv2.line(img,(xp,yp),(x1,y1),paint_colors,5)
            cv2.line(img_canvas,(xp,yp),(x1,y1),paint_colors,5)

            xp,yp=x1,y1



    img=cv2.addWeighted(img,0.5,img_canvas,0.5,0)

    cv2.imshow("Video",img)
    cv2.imshow("Canvas", img_canvas)
    # print(img.shape)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
cap.release()