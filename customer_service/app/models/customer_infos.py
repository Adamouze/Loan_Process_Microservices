from pydantic import BaseModel
from datetime import datetime

class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: str
    class Config:
        orm_mode = True

class AccountResponse(BaseModel):
    id: int
    account_number: str
    balance: float
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True


class BankResponse(BaseModel):
    id: int
    name: str
    cashier_check_validity_pattern: str
    class Config:
        orm_mode = True

class BankingTransactionResponse(BaseModel):
    id: int
    transaction_type: str
    amount: float
    transaction_date: datetime
    class Config:
        orm_mode = True