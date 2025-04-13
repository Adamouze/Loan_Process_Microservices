import os
import requests
from app.models.notification import NotificationRequest, NotificationResponse

NOTIFICATION_PORT = os.getenv("NOTIFICATION_PORT")

if not NOTIFICATION_PORT:
    raise ValueError("NOTIFICATION_PORT environment variable is not set.")

url = f"http://notification_service:{NOTIFICATION_PORT}/notifier/notify"

def send_notification_service(notification: NotificationRequest) -> NotificationResponse:
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=notification, headers=headers)
    response.raise_for_status()
    return NotificationResponse(**response.json())