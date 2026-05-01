import os
from dotenv import load_dotenv

load_dotenv()

HEAD_TURN_THRESHOLD = float(os.getenv("HEAD_TURN_THRESHOLD", "0.07"))
HEAD_TURN_DURATION = float(os.getenv("HEAD_TURN_DURATION", "1.0"))
MIN_DISTANCE = float(os.getenv("MIN_DISTANCE", "1.0"))
DEVICE_CONFIDENCE = float(os.getenv("DEVICE_CONFIDENCE", "0.25"))
LOG_FILE = os.getenv("LOG_FILE", "logs/incidents.txt")
ALERT_SOUND = os.getenv("ALERT_SOUND", "true").lower() == "true"
PROXIMITY_PIXEL_THRESHOLD = int(os.getenv("PROXIMITY_PIXEL_THRESHOLD", "150"))
NO_FACE_DURATION = float(os.getenv("NO_FACE_DURATION", "3.0"))
