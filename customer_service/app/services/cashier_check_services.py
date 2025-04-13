from app.orm.orm import CashierCheck as CashierCheckORM, Account as AccountORM, Bank as BankORM
from app.models.cashier_check import CashierCheckCreate, CashierCheckGenerate, CashierCheckGenerateResponse
from sqlalchemy.orm import Session
from app.error_handling.error_types import NotFoundError
import requests
import random
import re
import os
from datetime import datetime, timedelta

# generate a cashier check
def generate_cashier_check(cashier_check: CashierCheckGenerate, db: Session):
    # Check if the account exists
    account = db.query(AccountORM).filter(AccountORM.account_number == cashier_check.account_number).first()
    if not account:
        raise NotFoundError("Account not found")
    
    # Check if the bank exists
    bank = db.query(BankORM).filter(BankORM.id == account.bank_id).first()
    if not bank:
        raise NotFoundError("Bank not found")
    
    # Generate a unique account number based on the bank's account number validity pattern
    pattern = bank.cashier_check_validity_pattern
    while True:
        # Replace placeholders in the pattern with random digits
        generated_check_number = re.sub(r'\[0-9\]\{(\d+)\}', 
                        lambda x: ''.join(random.choices('0123456789', k=int(x.group(1)))), 
                        pattern)
        # Check if the generated account number is unique
        existing_check_number = db.query(CashierCheckORM).filter(CashierCheckORM.check_number == generated_check_number).first()
        if not existing_check_number:
            break

    # Generate a date that is today's date + 1 month
    generated_check_date = datetime.now() + timedelta(days=30)
    
    # Generate a cashier check
    generated_check = CashierCheckGenerateResponse(
        account_number=cashier_check.account_number,
        check_number=generated_check_number,
        issue_date=generated_check_date,
        amount=cashier_check.amount
    )
    
    return generated_check
    
def submit_cashier_check(cashier_check: CashierCheckCreate, db: Session):
    # Check if the account exists
    account = db.query(AccountORM).filter(AccountORM.account_number == cashier_check.account_number).first()
    if not account:
        raise NotFoundError("Account not found")

    cashier_check_to_create = CashierCheckORM(
        account_id=account.id,
        check_number=cashier_check.check_number,
        issue_date=cashier_check.issue_date,
        amount=cashier_check.amount,
        is_valid=cashier_check.is_valid
    )

    db.add(cashier_check_to_create)
    db.commit()
    db.refresh(cashier_check_to_create)

    return cashier_check_to_create


# Get cashier check by check number
def get_cashier_check(check_number: str, db: Session):
    cashier_check = db.query(CashierCheckORM).filter(CashierCheckORM.check_number == check_number).first()
    if not cashier_check:
        raise NotFoundError("Cashier check not found")
    return cashier_check
    
# Get all cashier checks for an account
def get_cashier_checks_by_account_number(account_number: str, db: Session):
    # Check if the account exists
    account = db.query(AccountORM).filter(AccountORM.account_number == account_number).first()
    if not account:
        raise NotFoundError("Account not found")
    
    # Get cashier checks for the account
    cashier_checks = db.query(CashierCheckORM).filter(CashierCheckORM.account_id == account.id).all()
    if not cashier_checks:
        raise NotFoundError("No cashier checks found for this account number")
    
    return cashier_checks

# Delete a cashier check
def delete_cashier_check(check_number: str, db: Session):
    cashier_check = db.query(CashierCheckORM).filter(CashierCheckORM.check_number == check_number).first()
    if not cashier_check:
        raise NotFoundError("Cashier check not found")
    
    db.delete(cashier_check)
    db.commit()
    
    return {"message": "Cashier check deleted successfully"}