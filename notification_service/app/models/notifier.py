from pydantic import BaseModel

class NotificationRequest(BaseModel):
    sender_address: str
    message: str