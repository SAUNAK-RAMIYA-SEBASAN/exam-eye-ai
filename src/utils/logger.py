import os

def get_timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_incident(incident_type, details):
    os.makedirs("logs", exist_ok=True)
    from config.settings import LOG_FILE
    with open(LOG_FILE, "a") as f:
        f.write(f"[{get_timestamp()}] {incident_type}: {details}\n")
