from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.account_services import get_account_details_by_id, get_account_details_by_account_number
from ..models.customer_infos import AccountResponse

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    try:
        return get_account_details_by_id(account_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/by-number/{account_number}", response_model=AccountResponse)
def get_account_by_number(account_number: str, db: Session = Depends(get_db)):
    try:
        return get_account_details_by_account_number(account_number, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))