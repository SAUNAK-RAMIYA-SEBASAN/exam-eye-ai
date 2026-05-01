## Exam-Eye-AI

### Goal

Build a real-time exam malpractice detection system in this order:

1. Head pose detection
2. Proximity detection
3. Device detection
4. Logging and alerts
5. Live dashboard with visualization

### Stack

• Python 3.11
• uv for environment and dependency management
• OpenCV for video processing
• MediaPipe for head pose detection
• YOLOv8 for object detection (phones/devices)
• NumPy for calculations
• python-dotenv for configuration

### Structure

• `src/detectors/head_pose_detector.py` - detect head rotation angles
• `src/detectors/proximity_detector.py` - measure distance between students
• `src/detectors/device_detector.py` - detect unauthorized devices
• `src/utils/logger.py` - incident logging
• `src/utils/alerts.py` - alert system
• `src/utils/visualization.py` - video annotation and display
• `src/config/settings.py` - thresholds and configuration
• `src/main.py` - main execution pipeline

### Project Structure

```
exam-eye-ai/
│
├── .venv/
├── .env
│
├── src/
│   ├── detectors/
│   │   ├── head_pose_detector.py
│   │   ├── proximity_detector.py
│   │   └── device_detector.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── alerts.py
│   │   └── visualization.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   └── main.py
│
├── logs/
│   └── incidents.txt
│
├── requirements.txt
```

### Rules

• Keep code modular and follow best practices and use the .env files when needed and no emojis should be used in the code
• Binary classification (flag/no-flag) based on thresholds only
• Test each detector independently before integration
• All detections must include timestamp and location data
• Alerts must trigger immediately upon violation
• Logging must include incident type, timestamp, and confidence
• No complex probability scoring; use simple threshold logic
• UI should be minimal and show real-time feed with bounding boxes

### Configuration (config/settings.py)

• `HEAD_TURN_THRESHOLD = 25` degrees
• `HEAD_TURN_DURATION = 2.0` seconds
• `MIN_DISTANCE = 1.0` meters
• `DEVICE_CONFIDENCE = 0.5` confidence threshold
• `LOG_FILE = "logs/incidents.txt"`
• `ALERT_SOUND = True`

### Run

• Main pipeline: `uv run src/main.py`
• Head pose detector: `uv run src/detectors/head_pose_detector.py`
• Proximity detector: `uv run src/detectors/proximity_detector.py`
• Device detector: `uv run src/detectors/device_detector.py`
