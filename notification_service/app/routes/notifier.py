from fastapi import APIRouter
from models.notifier import NotificationRequest
from services.notifier_service import send_notification

router = APIRouter(
    prefix="/notifier",
    tags=["notifier"]
)

@router.post("/notify")
def notify(payload: NotificationRequest):
    send_notification_response = send_notification(payload)
    return send_notification_response
