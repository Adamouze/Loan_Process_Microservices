from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..services.banking_transactions_services import get_transaction_by_id, get_transactions_by_account_number, get_transactions_by_type_and_account
from ..models.customer_infos import BankingTransactionResponse

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.get("/{transaction_id}", response_model=BankingTransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    try:
        return get_transaction_by_id(transaction_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/account/{account_number}/type/{transaction_type}", response_model=List[BankingTransactionResponse])
def get_account_transactions_by_type(account_number: str, transaction_type: str, db: Session = Depends(get_db)):
    try:
        return get_transactions_by_type_and_account(account_number, transaction_type, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/account/{account_number}", response_model=List[BankingTransactionResponse])
def get_account_transactions(account_number: str, db: Session = Depends(get_db)):
    try:
        return get_transactions_by_account_number(account_number, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))