from pydantic import BaseModel

class NotificationRequest(BaseModel):
    receiver_address: str
    message: str