import cv2
import numpy as np

def draw_violation_box(frame, text, box_color=(0, 0, 255)):
    height, width = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (width, 60), box_color, -1)
    cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def draw_detection_box(frame, label, x1, y1, x2, y2, color=(0, 255, 0)):
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def display_frame(frame, title="Exam Eye AI"):
    cv2.imshow(title, frame)
