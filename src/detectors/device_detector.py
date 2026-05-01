import cv2
from ultralytics import YOLO
from config.settings import DEVICE_CONFIDENCE
from utils.logger import log_incident
from utils.alerts import send_alert

class DeviceDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.device_classes = [67, 63]

    def detect(self, frame):
        results = self.model(frame, conf=DEVICE_CONFIDENCE, verbose=False)[0]
        violations = []
        for box in results.boxes:
            cls = int(box.cls[0])
            if cls in self.device_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                label = f"Device {conf:.2f}"
                violations.append((x1, y1, x2, y2, label))
                log_incident("DEVICE", f"Detected device with confidence {conf:.2f}")
                send_alert("DEVICE", f"Detected device with confidence {conf:.2f}")
        return violations

    def draw(self, frame, violations):
        for x1, y1, x2, y2, label in violations:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return frame

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = DeviceDetector()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        violations = detector.detect(frame)
        frame = detector.draw(frame, violations)
        if violations:
            cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 10)
        cv2.imshow("Device Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
