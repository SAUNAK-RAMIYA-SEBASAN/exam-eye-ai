import cv2
import mediapipe as mp
import numpy as np
import time
from config.settings import HEAD_TURN_THRESHOLD, HEAD_TURN_DURATION, NO_FACE_DURATION
from utils.logger import log_incident
from utils.alerts import send_alert

class HeadPoseDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.violation_start = None
        self.alerted = False
        self.no_face_start = None
        self.no_face_alerted = False

    def get_head_angle(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        if not results.multi_face_landmarks:
            return None
        landmarks = results.multi_face_landmarks[0].landmark
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        nose_tip = landmarks[1]
        face_width = abs(right_eye.x - left_eye.x)
        if face_width < 0.01:
            return None
        face_center_x = (left_eye.x + right_eye.x) / 2
        nose_offset_x = (nose_tip.x - face_center_x) / face_width
        return nose_offset_x

    def detect(self, frame):
        offset = self.get_head_angle(frame)
        if offset is None:
            if self.no_face_start is None:
                self.no_face_start = time.time()
            elapsed = time.time() - self.no_face_start
            if elapsed >= NO_FACE_DURATION:
                if not self.no_face_alerted:
                    log_incident("NO_FACE", "No face detected in frame")
                    send_alert("NO_FACE", "No face detected in frame")
                    self.no_face_alerted = True
                return False
            return False
        self.no_face_start = None
        self.no_face_alerted = False
        deviation = abs(offset)
        if deviation > HEAD_TURN_THRESHOLD:
            if self.violation_start is None:
                self.violation_start = time.time()
            elapsed = time.time() - self.violation_start
            if elapsed >= HEAD_TURN_DURATION:
                if not self.alerted:
                    log_incident("HEAD_TURN", f"Head turned {deviation:.1f} degrees")
                    send_alert("HEAD_TURN", f"Head turned {deviation:.1f} degrees")
                    self.alerted = True
                return True
            return False
        else:
            self.violation_start = None
            self.alerted = False
            return False

    def draw(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, landmarks, self.mp_face_mesh.FACEMESH_CONTOURS
                )
        return frame

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = HeadPoseDetector()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = detector.draw(frame)
        violation = detector.detect(frame)
        if violation:
            cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 10)
        cv2.imshow("Head Pose Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
