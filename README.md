# Exam Eye AI

<h1 align="center">Exam Eye AI</h1>

<p align="center">
  Real-time exam malpractice detection system using computer vision
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB"/>
  <img src="https://img.shields.io/badge/Stack-uv-FASTAPI"/>
  <img src="https://img.shields.io/badge/Detection-OpenCV-MediumSeaGreen"/>
  <img src="https://img.shields.io/badge/Detection-MediaPipe-FBBBBB"/>
  <img src="https://img.shields.io/badge/Detection-YOLOv8-Red"/>
</p>

---

## Overview

Exam Eye AI is a real-time exam malpractice detection system that monitors students during examinations using computer vision. It detects suspicious behaviors like head tilts, device usage, proximity violations, and absence of face in the camera frame.

---

## Features

### 1. Head Pose Detection
Monitors the student's head orientation. Looking left or right for a sustained period triggers a violation. Looking down (while writing) is considered normal behavior and is not flagged.

**Detection method:** Uses MediaPipe Face Mesh to track facial landmarks and calculates nose offset from face center.

### 2. No Face Detection
Flags when the student's face is not visible in the camera frame for a configurable duration.

**Detection method:** Monitors face mesh detection; absence of face for the threshold duration triggers an alert.

### 3. Device Detection
Detects unauthorized devices (mobile phones, laptops) in the examination area using YOLOv8 object detection.

**Detection method:** YOLOv8 trained on COCO dataset, detects class 67 (cell phone) and class 63 (laptop).

### 4. Proximity Detection
Detects when two students are sitting too close to each other by measuring pixel distance between face centers.

**Detection method:** Calculates distance between face centers from MediaPipe landmarks; flags if distance falls below threshold.

---

## Violation Types

| Violation | Trigger Condition | Default Threshold |
|-----------|------------------|-------------------|
| **HEAD_TURN** | Head turned left/right (nose offset from center) sustained for duration | Offset > 0.07 for 1.0 second |
| **NO_FACE** | No face detected in camera frame | 3.0 seconds |
| **DEVICE** | Mobile phone or laptop detected | Confidence > 0.25 |
| **PROXIMITY** | Two faces within pixel distance threshold | Distance < 150 pixels |

---

## Tech Stack

* **Python 3.11** - Programming language
* **uv** - Package manager and environment tool
* **OpenCV** - Video processing
* **MediaPipe** - Face landmark detection
* **YOLOv8** - Object detection (devices)
* **NumPy** - Numerical calculations
* **python-dotenv** - Configuration management

---

## Project Structure

```
exam-eye/
|
├── src/
│   ├── detectors/
│   │   ├── head_pose_detector.py   # Head turn + no face detection
│   │   ├── proximity_detector.py   # Multi-student proximity detection
│   │   └── device_detector.py      # Phone/laptop detection
│   │
│   ├── utils/
│   │   ├── logger.py               # Incident logging
│   │   ├── alerts.py               # Alert system
│   │   └── visualization.py        # Video annotation
│   │
│   ├── config/
│   │   └── settings.py             # Configuration & thresholds
│   │
│   └── main.py                     # Main pipeline
│
├── logs/
│   └── incidents.txt               # Incident log file
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Setup and Installation

### Prerequisites

* Python 3.11 or higher installed
* Webcam camera connected
* Git installed

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/exam-eye-ai.git
cd exam-eye-ai
```

---

### Step 2: Install uv (if not installed)

```bash
# On Windows (using PowerShell)
powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### Step 3: Create and Configure Environment File

Create a file named `.env` in the project root directory (same level as `requirements.txt`):

```bash
# Copy the example below and save as .env
```

**.env file content:**

```
HEAD_TURN_THRESHOLD=0.07
HEAD_TURN_DURATION=1.0
MIN_DISTANCE=1.0
DEVICE_CONFIDENCE=0.25
LOG_FILE=logs/incidents.txt
ALERT_SOUND=true
PROXIMITY_PIXEL_THRESHOLD=150
NO_FACE_DURATION=3.0
```

---

### Step 4: Install Dependencies

```bash
uv sync
```

This will create a virtual environment and install all packages from `requirements.txt`.

---

## Running the Application

### Full Pipeline (All Detectors)

```bash
uv run python src/main.py
```

### Individual Detectors (for testing)

```bash
# Head pose + no face detection only
uv run python src/detectors/head_pose_detector.py

# Proximity detection only
uv run python src/detectors/proximity_detector.py

# Device detection only
uv run python src/detectors/device_detector.py
```

### Quit

Press `q` to quit the application.

---

## Configuration

All settings are controlled via the `.env` file:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `HEAD_TURN_THRESHOLD` | Sensitivity for head turn detection (lower = more sensitive) | 0.07 |
| `HEAD_TURN_DURATION` | Seconds the head must be turned before flagging | 1.0 |
| `DEVICE_CONFIDENCE` | Minimum confidence for device detection (0.0 to 1.0) | 0.25 |
| `PROXIMITY_PIXEL_THRESHOLD` | Maximum pixel distance between faces before flagging | 150 |
| `NO_FACE_DURATION` | Seconds without face detection before flagging | 3.0 |
| `LOG_FILE` | Path to incident log file | logs/incidents.txt |
| `ALERT_SOUND` | Play sound on violation (true/false) | true |

---

## Incident Logging

All violations are logged to `logs/incidents.txt` with timestamp, incident type, and details:

```
[2026-05-01 12:34:56] HEAD_TURN: Head turned sideways, offset: 0.123
[2026-05-01 12:35:02] NO_FACE: No face detected in frame
[2026-05-01 12:35:10] DEVICE: Detected device with confidence 0.87
[2026-05-01 12:35:15] PROXIMITY: Distance 120.5px below threshold
```

---

## How It Works

### Head Turn Detection
1. MediaPipe extracts 468 facial landmarks
2. Face center is calculated from left eye (landmark 33) and right eye (landmark 263)
3. Nose tip (landmark 1) horizontal offset from face center is measured
4. Offset is normalized by face width to be consistent regardless of camera distance
5. If offset exceeds threshold for sustained duration, violation is flagged

**Note:** Looking down while writing is NOT flagged because the nose moves vertically but the horizontal offset remains near zero.

### No Face Detection
1. MediaPipe face mesh runs continuously on each frame
2. If no face landmarks detected, a timer starts
3. After the timer exceeds `NO_FACE_DURATION`, violation is flagged
4. Timer resets immediately when a face is re-detected

### Device Detection
1. YOLOv8 processes each frame with configurable confidence threshold
2. Detections are filtered to only class 67 (cell phone) and class 63 (laptop)
3. If a device is detected, bounding box is drawn and violation is logged

### Proximity Detection
1. MediaPipe detects up to 10 faces simultaneously
2. Face center is calculated for each detected face
3. Pixel distance between all face pairs is computed
4. If any pair is closer than `PROXIMITY_PIXEL_THRESHOLD`, violation is flagged

---

## Troubleshooting

**Issue: ModuleNotFoundError: No module named 'src'**
```bash
# Make sure you are running from the project root
cd exam-eye-ai
uv run python src/main.py
```

**Issue: Camera not found**
```bash
# Check camera index (0 is usually the default webcam)
# Try changing the index in main.py if you have multiple cameras
cap = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc.
```

**Issue: YOLO model download fails**
```bash
# The model downloads automatically on first run
# If it fails, manually download from:
# https://github.com/ultralytics/ultralytics
```

**Issue: Permission denied when creating logs**
```bash
# Create the logs directory manually
mkdir logs
```

---

## License

MIT License
