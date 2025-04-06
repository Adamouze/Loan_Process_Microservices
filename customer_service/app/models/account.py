from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

class AccountCreate(BaseModel):
    bank_name : str # This will be used to get the bank_id
    full_name: str # This will be used to get the customer_id	
    balance: Decimal = Field(..., max_digits=15, decimal_places=2)

class AccountUpdate(BaseModel):
    id: int
    full_name: Optional[str] = None # This will be used to get the customer_id
    bank_name : Optional[str] = None # This will be used to get the bank_id
    balance: Optional[Decimal] = None

class AccountResponse(BaseModel):
    id: int
    customer_id: int
    bank_id: int
    account_number: str
    balance: Decimal = Field(..., max_digits=15, decimal_places=2)
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


