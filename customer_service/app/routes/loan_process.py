from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.services.loan_process_services import loan_process_service_first_part
from ..models.loan_application_and_monitoring import (
    Loan_ApplicationCreate,
    Loan_Application_with_MonitoringResponse
)

router = APIRouter(
    prefix="/loan-process",
    tags=["loan-process"]
)

@router.post("/", response_model=Loan_Application_with_MonitoringResponse)
def loan_process_first_part(loan_application: Loan_ApplicationCreate, db: Session = Depends(get_db)):
    return loan_process_service_first_part(loan_application, db)
