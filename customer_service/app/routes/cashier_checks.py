from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.cashier_check_services import submit_cashier_check, get_cashier_check
from ..models.cashier_check import CashierCheckCreate, CashierCheckResponse

router = APIRouter(
    prefix="/cashier-checks",
    tags=["cashier-checks"]
)

@router.post("/", response_model=dict)
def create_cashier_check(cashier_check: CashierCheckCreate):
    try:
        return submit_cashier_check(cashier_check)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{check_number}", response_model=CashierCheckResponse)
def get_check(check_number: str, db: Session = Depends(get_db)):
    try:
        return get_cashier_check(check_number, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))