from fastapi import APIRouter
from models.notifier import NotificationRequest
from services.notifier_service import send_notification

router = APIRouter(
    prefix="/notifier",
    tags=["notifier"]
)

@router.post("/notify")
def notify(payload: NotificationRequest):
    success = send_notification(payload.sender_address, payload.message)
    return {"status": "success" if success==202 else "failed"}