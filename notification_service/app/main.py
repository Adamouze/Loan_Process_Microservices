from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from app.notifier.service import send_notification
import os

NOTIFICATION_PORT = int(os.getenv("NOTIFICATION_PORT"))

if not NOTIFICATION_PORT or NOTIFICATION_PORT <= 0:
    raise ValueError("NOTIFICATION_PORT environment variable not set.")

app = FastAPI()

class NotificationRequest(BaseModel):
    phone_number: str
    message: str

@app.post("/notify")
def notify(payload: NotificationRequest):
    success = send_notification(payload.phone_number, payload.message)
    return {"status": "sent" if success else "failed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=NOTIFICATION_PORT)

