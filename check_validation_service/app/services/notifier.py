import requests
import os

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8000")

def notify_bounced_check(phone_number: str, message: str) -> bool:
    try:
        response = requests.post(
            f"{NOTIFICATION_SERVICE_URL}/notify",
            json={"phone": phone_number, "message": message},
            timeout=5
        )
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Notification failed: {e}")
        return False
