from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class CashierCheckGenerate(BaseModel):
    account_number: str # `account_number` corresponds to `account_id` in the table
    amount: Decimal = Field(..., max_digits=15, decimal_places=2)

class CashierCheckGenerateResponse(CashierCheckGenerate):
    check_number: str
    issue_date: datetime

class CashierCheckBase(CashierCheckGenerateResponse):
    pass

class CashierCheckCreate(CashierCheckBase):
    is_valid: Optional[bool] = True
    pass

class CashierCheckResponse(BaseModel):
    id: int
    account_id: int
    check_number: str
    amount: Decimal = Field(..., max_digits=15, decimal_places=2)
    issue_date: datetime
    is_valid: bool
    created_at: datetime
    class Config:
        from_attributes = True