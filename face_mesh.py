import cv2,time
import mediapipe as mp


class face_mesh():
    def __init__(self,mode=False,no_of_faces=1,detection_confidence=0.5,tracking_confidence=0.5):
        self.mode=mode
        self.no_of_faces=no_of_faces
        self.detection_confidence=detection_confidence
        self.tracking_confidence=tracking_confidence
        self.mp_draw=mp.solutions.drawing_utils
        self.mp_face_mesh=mp.solutions.face_mesh
        self.face_mesh=self.mp_face_mesh.FaceMesh(self.mode,self.no_of_faces,self.detection_confidence,self.tracking_confidence)
        self.draw_spec=self.mp_draw.DrawingSpec(thickness=1,circle_radius=1,color=(0,255,0))


    def find_face_mesh(self,img,draw=True):
        img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.face_mesh.process(img_rgb)
        faces = []
        if self.results.multi_face_landmarks:

            for face_lm in self.results.multi_face_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img,face_lm,self.mp_face_mesh.FACE_CONNECTIONS,self.draw_spec,self.draw_spec)
                face = []
                for id, lm in enumerate(face_lm.landmark):
                    # print(id,lm)
                    height, width, channel = img.shape
                    cx, cy = int(lm.x * width), int(lm.y * height)
                    # print(id, cx, cy)
                    face.append([id,cx,cy])
                faces.append(face)
        return img,faces




def main():
    cap = cv2.VideoCapture(0)
    current_time = 0
    prev_time = 0
    detector=face_mesh()
    while True:
        success, img = cap.read()

        img,faces=detector.find_face_mesh(img)
        if len(faces)!=0:
            print(faces[0][0]) #first face first point

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(img, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (20, 0, 0), 3)

        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()

if __name__=="__main__":
    main()