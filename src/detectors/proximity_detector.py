import cv2
import numpy as np
from config.settings import PROXIMITY_PIXEL_THRESHOLD
from utils.logger import log_incident
from utils.alerts import send_alert

class ProximityDetector:
    def __init__(self, pixel_threshold=None):
        self.pixel_threshold = pixel_threshold if pixel_threshold is not None else PROXIMITY_PIXEL_THRESHOLD

    def detect(self, face_centers):
        if not face_centers or len(face_centers) < 2:
            return False
        for i in range(len(face_centers)):
            for j in range(i + 1, len(face_centers)):
                x1, y1 = face_centers[i]
                x2, y2 = face_centers[j]
                dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist < self.pixel_threshold:
                    log_incident("PROXIMITY", f"Distance {dist:.1f}px below threshold")
                    send_alert("PROXIMITY", f"Distance {dist:.1f}px below threshold")
                    return True
        return False

if __name__ == "__main__":
    import mediapipe as mp
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=10)
    cap = cv2.VideoCapture(0)
    detector = ProximityDetector()
    cv2.namedWindow("Proximity Detector")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        face_centers = []
        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                left_eye = landmarks.landmark[33]
                right_eye = landmarks.landmark[263]
                x1 = int(left_eye.x * w)
                x2 = int(right_eye.x * w)
                fc_x = (x1 + x2) // 2
                fc_y = int(((left_eye.y + right_eye.y) / 2) * h)
                face_centers.append((fc_x, fc_y))
                cv2.line(frame, (x1, int(left_eye.y * h)), (x2, int(right_eye.y * h)), (0, 255, 0), 2)
        violation = detector.detect(face_centers)
        if violation:
            cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 10)
        cv2.imshow("Proximity Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
