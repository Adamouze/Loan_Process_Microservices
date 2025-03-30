from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CashierCheckBase(BaseModel):
    account_number: str # `account_number` corresponds to `account_id` in the table
    bank_name: str  # `bank_name` corresponds to `bank_id` in the table
    check_number: str
    issue_date: datetime
    amount: float

class CashierCheckCreate(CashierCheckBase):
    pass

class CashierCheckResponse(CashierCheckBase):
    id: int
    account_id: int
    bank_id: int
    is_valid: bool
    created_at: datetime
    class Config:
        orm_mode = True