import requests

NOTIFICATION_SERVICE_URL = "http://notification_service:8004/notify"  # Docker name + port

def send_sms_notification(phone_number: str, message: str):
    try:
        response = requests.post(
            NOTIFICATION_SERVICE_URL,
            json={"phone_number": phone_number, "message": message},
            timeout=5
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")
