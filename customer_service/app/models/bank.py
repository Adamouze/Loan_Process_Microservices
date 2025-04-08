from pydantic import BaseModel

class BankResponse(BaseModel):
    id: int
    name: str
    account_number_validity_pattern: str
    cashier_check_validity_pattern: str
    class Config:
        from_attributes = True