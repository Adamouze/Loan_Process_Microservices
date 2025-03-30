from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..services.bank_services import get_bank_details_by_id, get_bank_details_by_name, get_all_banks
from ..models.customer_infos import BankResponse

router = APIRouter(
    prefix="/banks",
    tags=["banks"]
)

@router.get("/{bank_id}", response_model=BankResponse)
def get_bank_by_id(bank_id: int, db: Session = Depends(get_db)):
    try:
        return get_bank_details_by_id(bank_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/by-name/{bank_name}", response_model=BankResponse)
def get_bank_by_name(bank_name: str, db: Session = Depends(get_db)):
    try:
        return get_bank_details_by_name(bank_name, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[BankResponse])
def get_banks(db: Session = Depends(get_db)):
    try:
        return get_all_banks(db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))