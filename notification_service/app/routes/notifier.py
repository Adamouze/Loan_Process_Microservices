from fastapi import APIRouter
from models.notifier import NotificationRequest
from services.notifier_service import send_notification

router = APIRouter(
    prefix="/notifier",
    tags=["notifier"]
)

@router.post("/notify")
def notify(payload: NotificationRequest):
    success = send_notification(payload.receiver_address, payload.message)
    return {"status": "message sent successfully" if success==202 else "message failed"}
