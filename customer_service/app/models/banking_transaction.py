from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from decimal import Decimal

class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"

class BankingTransactionCreate(BaseModel):
    account_number: str # This will be used to get the account_id
    transaction_type: TransactionType
    amount: Decimal = Field(..., max_digits=15, decimal_places=2)

class BankingTransactionResponse(BaseModel):
    id: int
    account_id: int
    transaction_type: TransactionType
    amount: Decimal = Field(..., max_digits=15, decimal_places=2)
    transaction_date: datetime
    class Config:
        from_attributes = True