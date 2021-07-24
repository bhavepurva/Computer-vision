import cv2, time
import mediapipe as mp

class hand_tracker():
    def __init__(self,mode=False,max_hands=2,detection_confidence=0.5,tracking_confidence=0.5):
        self.mode=mode
        self.max_hands=max_hands
        self.detection_confidence=detection_confidence
        self.tracking_confidence=tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,self.max_hands,self.detection_confidence,self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils  # helps to draw landmarks
        self.tip_ids=[4,8,12,16,20]

    def find_hands(self,img,draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # hands class uses rgb images only
        self.results = self.hands.process(img_rgb)  # grabs hands detected
        # print(results.multi_hand_landmarks) #we get values if hand is detected
        if self.results.multi_hand_landmarks:  # checks if hands exist
            for hand_lm in self.results.multi_hand_landmarks:
                # get id no and landmark info(x,y coord) for each  hand
               if draw:
                    self.mp_draw.draw_landmarks(img, hand_lm, self.mp_hands.HAND_CONNECTIONS)  # single hand, draw landmarks
        return img

    def find_position(self,img,hand_no=0,draw=True):
        self.lm_list=[]
        if self.results.multi_hand_landmarks:  # checks if hands exist
            my_hand=self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):  # gets each red point landmark
                # each id will have x,y,z coords, these are ratio values, we multiply them with width and height which will give us pixel location
                # these values are dec, but  location has to be in pixels
                height, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                # print(id, cx, cy)
                self.lm_list.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)  # circle at 0th landmark
        return self.lm_list

    def fingers_that_are_up(self):
        fingers=[]
        if self.lm_list[self.tip_ids[0]][1]<self.lm_list[self.tip_ids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if self.lm_list[self.tip_ids[id]][2]<self.lm_list[self.tip_ids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

def main():
    prev_time = 0
    current_time = 0
    cap = cv2.VideoCapture(0)
    detector=hand_tracker()
    while True:
        success, img = cap.read()
        img=detector.find_hands(img)
        lm_list=detector.find_position(img,draw=False)
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0))

        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if len(lm_list)!=0:
            print(lm_list[5])
    cap.release()


if __name__=="__main__":
    main()