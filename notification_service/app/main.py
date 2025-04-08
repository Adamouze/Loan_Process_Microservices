from fastapi import FastAPI
from pydantic import BaseModel
from app.notifier.service import send_notification

app = FastAPI()

class NotificationRequest(BaseModel):
    phone_number: str
    message: str

@app.post("/notify")
def notify(payload: NotificationRequest):
    success = send_notification(payload.phone_number, payload.message)
    return {"status": "sent" if success else "failed"}
