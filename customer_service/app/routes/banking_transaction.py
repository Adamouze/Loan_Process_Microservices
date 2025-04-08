from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..services.banking_transactions_services import get_transaction_by_id, get_transactions_by_account_number, get_transactions_by_type_and_account, create_banking_transaction
from ..models.banking_transaction import BankingTransactionResponse, BankingTransactionCreate

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/", response_model=BankingTransactionResponse)
def create_transaction(banking_transaction: BankingTransactionCreate, db: Session = Depends(get_db)):
    return create_banking_transaction(banking_transaction, db)

@router.get("/{transaction_id}", response_model=BankingTransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return get_transaction_by_id(transaction_id, db)
    
@router.get("/account/{account_number}/type/{transaction_type}", response_model=List[BankingTransactionResponse])
def get_account_transactions_by_type(account_number: str, transaction_type: str, db: Session = Depends(get_db)):
    return get_transactions_by_type_and_account(account_number, transaction_type, db)

@router.get("/account/{account_number}", response_model=List[BankingTransactionResponse])
def get_account_transactions(account_number: str, db: Session = Depends(get_db)):
    return get_transactions_by_account_number(account_number, db)