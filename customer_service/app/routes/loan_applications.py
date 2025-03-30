from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..services.loan_application_services import (
    create_loan_application, 
    create_loan_application_with_monitoring,
    get_loan_application_by_id,
    get_loan_applications_by_account_number,
    get_loan_application_with_monitoring
)
from ..models.loan_application import (
    Loan_ApplicationCreate, 
    Loan_ApplicationResponse,
    Loan_Application_with_MonitoringResponse
)

router = APIRouter(
    prefix="/loan-applications",
    tags=["loan-applications"]
)

@router.post("/", response_model=Loan_ApplicationResponse)
def create_loan(loan_application: Loan_ApplicationCreate, db: Session = Depends(get_db)):
    try:
        return create_loan_application(loan_application, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/with-monitoring", response_model=Loan_Application_with_MonitoringResponse)
def create_loan_with_monitoring(loan_application: Loan_ApplicationCreate, db: Session = Depends(get_db)):
    try:
        return create_loan_application_with_monitoring(loan_application, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{loan_id}", response_model=Loan_ApplicationResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    try:
        return get_loan_application_by_id(loan_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/account/{account_number}", response_model=List[Loan_ApplicationResponse])
def get_loans_by_account(account_number: str, db: Session = Depends(get_db)):
    try:
        return get_loan_applications_by_account_number(account_number, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{loan_id}/with-monitoring", response_model=Loan_Application_with_MonitoringResponse)
def get_loan_with_monitoring(loan_id: int, db: Session = Depends(get_db)):
    try:
        return get_loan_application_with_monitoring(loan_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))