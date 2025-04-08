from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from decimal import Decimal
from typing import Optional

class CustomerCreate(BaseModel):
    full_name: str
    email: str

class CustomerUpdate(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: str
    class Config:
        from_attributes = True