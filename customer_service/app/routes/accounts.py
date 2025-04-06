from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.account_services import get_account_details_by_id, get_account_details_by_account_number, get_all_accounts_by_customer_id, create_account as create_account_service, update_account as update_account_service, delete_account as delete_account_service
from ..models.account import  AccountCreate, AccountUpdate, AccountResponse
from typing import List

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account_service(account, db)
    
@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account: AccountUpdate, db: Session = Depends(get_db)):
    return update_account_service(account, db)
    

@router.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    return get_account_details_by_id(account_id, db)

@router.get("/by-number/{account_number}", response_model=AccountResponse)
def get_account_by_number(account_number: str, db: Session = Depends(get_db)):
    return get_account_details_by_account_number(account_number, db)
    
@router.get("/customer/{customer_id}", response_model=List[AccountResponse])
def get_accounts_by_customer(customer_id: int, db: Session = Depends(get_db)):
    return get_all_accounts_by_customer_id(customer_id, db)
    
@router.delete("/{account_id}", response_model=dict)
def delete_account_by_id(account_id: int, db: Session = Depends(get_db)):
    return delete_account_service(account_id, db)
    