from config.settings import ALERT_SOUND

def send_alert(incident_type, details):
    if ALERT_SOUND:
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONWARNING)
        except Exception:
            pass
    print(f"[ALERT] {incident_type}: {details}")
