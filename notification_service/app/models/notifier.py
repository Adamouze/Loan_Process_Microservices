from pydantic import BaseModel

class NotificationRequest(BaseModel):
    receiver_address: str
    message: str

class NotificationResponse(BaseModel):
    status: bool
    class Config:
        from_attributes = True