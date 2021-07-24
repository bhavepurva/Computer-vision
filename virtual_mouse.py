import cv2,time
import numpy as np
import hand_tracking as ht
import autopy,math

cam_width,cam_height=800,500
frame_reduction=100
smooth=10
prev_loc_x,prev_loc_y=0,0
current_loc_x,current_loc_y=0,0

cap=cv2.VideoCapture(0)
cap.set(3,cam_width)
cap.set(4,cam_height)

screen_width,screen_height=autopy.screen.size()  #1366.0, 768.0

detector=ht.hand_tracker(max_hands=1)


while True:
    success,img=cap.read()
    img=detector.find_hands(img)
    lm_list=detector.find_position(img,draw=False)

    if len(lm_list)!=0:
        x1,y1=lm_list[8][1],lm_list[8][2] #index
        x2,y2=lm_list[12][1],lm_list[12][2] #middle
        cv2.rectangle(img, (frame_reduction, frame_reduction),
                      (cam_width - frame_reduction, cam_height - frame_reduction), (255, 0, 0), 2)

        fingers=detector.fingers_that_are_up()
        if fingers[1]==True and fingers[2]==False:
            x3=np.interp(x1,(frame_reduction,cam_width-frame_reduction),(0,screen_width))
            y3=np.interp(y1,(frame_reduction,cam_height-frame_reduction),(0,screen_height))

            current_loc_x=prev_loc_x+(x3-prev_loc_x)/smooth
            current_loc_y = prev_loc_y + (y3 - prev_loc_y) / smooth
            autopy.mouse.move(screen_width-current_loc_x,current_loc_y)
            cv2.circle(img,(x1,y1),10,(255,255,255),cv2.FILLED)
            prev_loc_x,prev_loc_y=current_loc_x,current_loc_y

        if fingers[1]==True and fingers[2]==True:
            length=math.hypot(x2-x1,y2-y1)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cx,cy=(x1+x2)//2,(y1+y2)//2
            if length<=40:
                print("click")
                cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()


    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break