from pydantic import BaseModel
from enum import Enum

class LoanType(str, Enum):
        personal = "personal"
        commercial = "commercial"

class Loan_ApplicationBase(BaseModel):
    full_name: str
    account_number: str # `account_number` corresponds to `account_id` in the table
    loan_type: LoanType
    loan_amount: float
    loan_description: str

class Loan_ApplicationCreate(Loan_ApplicationBase):
    pass

class Loan_ApplicationResponse(Loan_ApplicationBase):    
    id: int
    customer_id: int
    account_id: int
    status: str
    created_at: str
    class Config:
        orm_mode = True

class Loan_Application_with_MonitoringResponse(Loan_ApplicationBase):
    Loan_Application : Loan_ApplicationResponse
    Loan_monitoring : dict