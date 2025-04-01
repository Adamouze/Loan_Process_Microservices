from pydantic import BaseModel, Field
from decimal import Decimal
from enum import Enum
from datetime import datetime

class LoanType(str, Enum):
    personal = "personal"
    commercial = "commercial"

# Loan application and monitoring models
class Loan_ApplicationBase(BaseModel):
    full_name: str
    account_number: str  # `account_number` corresponds to `account_id` in the table, we will use it to get the account_id
    loan_type: LoanType
    loan_amount: Decimal = Field(..., max_digits=15, decimal_places=2)
    loan_description: str

class LoanMonitoringBase(BaseModel):
    risk_status: str
    check_validation_status: str
    loan_provider_status: str
    notification_status: str
    customer_status: str

# Loan application and monitoring creation models
class Loan_ApplicationCreate(Loan_ApplicationBase):
    pass

class LoanMonitoringCreate(LoanMonitoringBase):
    loan_application_id: int

# Loan application and monitoring response models
class Loan_ApplicationResponse(BaseModel):    
    id: int
    customer_id: int
    account_id: int
    loan_type: LoanType
    loan_amount: Decimal = Field(..., max_digits=15, decimal_places=2)
    loan_description: str
    status: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class LoanMonitoringResponse(LoanMonitoringCreate):
    id: int
    monitoring_date: datetime
    class Config:
        orm_mode = True

# Loan application and monitoring response model with nested structure
class Loan_Application_with_MonitoringResponse(BaseModel):
    Loan_Application : Loan_ApplicationResponse
    Loan_Monitoring : LoanMonitoringResponse
    class Config:
        orm_mode = True