import cv2
import mediapipe as mp
import time


class pose_tracker():
    def __init__(self, mode=False, upper_body=False, smooth=True, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.upper_body = upper_body
        self.smooth = smooth
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.upper_body, self.smooth, self.detection_confidence,
                                      self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_pose(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return img

    def find_position(self, img, draw=True):
        lm_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                height, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (100, 0, 0), cv2.FILLED)
        return lm_list


def main():
    cap = cv2.VideoCapture("vid.mp4")
    prev_time = 0
    detector = pose_tracker()
    while True:
        success, img = cap.read()
        img = detector.find_pose(img)
        lm_list = detector.find_position(img, draw=False)
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        if len(lm_list)!=0:
            cv2.circle(img, (lm_list[15][1], lm_list[15][2]), 10, (100, 100, 0), cv2.FILLED)

        cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()


if __name__ == "__main__":
    main()
