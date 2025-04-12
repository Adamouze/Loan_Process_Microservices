from pydantic import BaseModel

class CheckValidationRequest(BaseModel):
    bank_id: int
    check_id: int
