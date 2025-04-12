from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.cashier_check_services import get_cashier_check, get_cashier_checks_by_account_number, delete_cashier_check as delete_cashier_check_service, generate_cashier_check as generate_cashier_check_service, submit_cashier_check as submit_cashier_check_service
from ..models.cashier_check import CashierCheckCreate, CashierCheckResponse, CashierCheckGenerate, CashierCheckGenerateResponse
from typing import List

router = APIRouter(
    prefix="/cashier-checks",
    tags=["cashier-checks"]
)

@router.post("/", response_model=CashierCheckGenerateResponse)
def generate_cashier_check(cashier_check_generate: CashierCheckGenerate, db: Session = Depends(get_db)):
    return generate_cashier_check_service(cashier_check_generate, db)

@router.post("/", response_model=CashierCheckResponse)
def submit_cashier_check(cashier_check: CashierCheckCreate):
    return submit_cashier_check_service(cashier_check)

@router.get("/{check_number}", response_model=CashierCheckResponse)
def get_check(check_number: str, db: Session = Depends(get_db)):
    return get_cashier_check(check_number, db)
    
@router.get("/account/{account_number}", response_model=List[CashierCheckResponse])
def get_checks_by_account(account_number: str, db: Session = Depends(get_db)):
    return get_cashier_checks_by_account_number(account_number, db)
    
@router.delete("/{check_number}", response_model=dict)
def delete_check(check_number: str, db: Session = Depends(get_db)):
    return delete_cashier_check_service(check_number, db)