import cv2
import mediapipe as mp
from detectors.head_pose_detector import HeadPoseDetector
from detectors.proximity_detector import ProximityDetector
from detectors.device_detector import DeviceDetector
from utils.visualization import draw_violation_box, display_frame
from utils.logger import log_incident

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    head_detector = HeadPoseDetector()
    proximity_detector = ProximityDetector()
    device_detector = DeviceDetector()

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=10)

    print("Exam Eye AI started. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        violations = {"head": False, "device": False, "proximity": False, "no_face": False}

        head_violation = head_detector.detect(frame)
        if head_violation:
            violations["head"] = True
        if head_detector.no_face_alerted:
            violations["no_face"] = True

        device_violations = device_detector.detect(frame)
        if device_violations:
            violations["device"] = True
            for x1, y1, x2, y2, label in device_violations:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        face_centers = []
        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                left_eye = landmarks.landmark[33]
                right_eye = landmarks.landmark[263]
                x1 = int(left_eye.x * w)
                x2 = int(right_eye.x * w)
                face_center_x = (x1 + x2) // 2
                face_center_y = int(((left_eye.y + right_eye.y) / 2) * h)
                face_centers.append((face_center_x, face_center_y))
                cv2.line(frame, (x1, int(left_eye.y * h)), (x2, int(right_eye.y * h)), (0, 255, 0), 2)

        proximity_violation = proximity_detector.detect(face_centers)
        if proximity_violation:
            violations["proximity"] = True

        if any(violations.values()):
            status = " | ".join([k.upper() for k, v in violations.items() if v])
            draw_violation_box(frame, f"VIOLATION: {status}")
            log_incident("MULTI", f"Violations: {status}")

        frame = head_detector.draw(frame)
        display_frame(frame, "Exam Eye AI")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
