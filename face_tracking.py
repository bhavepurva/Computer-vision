import cv2,time
import mediapipe as mp

class face_tracker():
    def __init__(self,min_detection_confidence=0.5):
        self.min_detection_confidence=min_detection_confidence

        self.mp_face=mp.solutions.face_detection
        self.face_detection=self.mp_face.FaceDetection(self.min_detection_confidence)
        self.mp_draw=mp.solutions.drawing_utils

    def find_face(self,img,draw=True):
        img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.face_detection.process(img_rgb)
        bbox=[]

        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
                val=detection.location_data.relative_bounding_box
                img_height,img_width,channel=img.shape
                bounding_box=int(val.xmin*img_width),int(val.ymin*img_height),int(val.width * img_width), int(val.height * img_height)
                # mp_draw.draw_detection(img,detection) #using mediapipe
                bbox.append([id,bounding_box,detection.score])
                if draw:
                    img=self.fancy_box(img,bounding_box)
                # cv2.rectangle(img,bounding_box,(0,10,10),2) #using our own code
                    cv2.putText(img,str(int(detection.score[0]*100)),(bounding_box[0],bounding_box[1]-20),cv2.FONT_HERSHEY_PLAIN,2,(0,10,10),2)
        return bbox,img

    def fancy_box(self,img,bbox,l=30,t=3):
        x,y,w,h=bbox
        x1,y1 =x+w,y+h #diagonal points

        cv2.line(img,(x,y),(x+l,y),(255,0,0),t)
        cv2.line(img, (x, y), (x , y+l), (255, 0, 0), t)

        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 0), t)
        cv2.line(img, (x1, y), (x1, y + l), (255, 0, 0), t)

        cv2.line(img, (x, y1), (x + l, y1), (255, 0, 0), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 0), t)

        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 0), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 0), t)
        return img


def main():
    cap = cv2.VideoCapture("vid.mp4")
    current_time = 0
    prev_time = 0
    detector=face_tracker()
    while True:
        success, img = cap.read()
        bbox,img=detector.find_face(img)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(img, str(int(fps)), (50, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Video", img)
        if len(bbox)!=0:
            print(bbox)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()


if __name__=="__main__":
    main()