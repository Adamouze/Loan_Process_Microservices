from sqlalchemy.orm import Session
from app.orm.orm import Customer as CustomerORM, Account as AccountORM, Bank as BankORM
from app.models.account import AccountCreate, AccountUpdate
from app.error_handling.error_types import NotFoundError
import random
import re
from datetime import datetime

# Create a new account
def create_account(account: AccountCreate, db: Session):
    # Check if the customer exists
    customer = db.query(CustomerORM).filter(CustomerORM.full_name == account.customer_id).first()
    if not customer:
        raise NotFoundError("Customer not found")
    
    # Check if the bank exists
    bank = db.query(BankORM).filter(BankORM.name == account.bank_name).first()
    if not bank:
        raise NotFoundError("Bank not found")
    
    # Generate a unique account number based on the bank's account number validity pattern
    pattern = bank.account_number_validity_pattern
    while True:
        # Replace placeholders in the pattern with random digits
        account_number = re.sub(r'\[0-9\]\{(\d+)\}', 
                        lambda x: ''.join(random.choices('0123456789', k=int(x.group(1)))), 
                        pattern)
        # Check if the generated account number is unique
        existing_account = db.query(AccountORM).filter(AccountORM.account_number == account_number).first()
        if not existing_account:
            break

    # Create a new account
    new_account = AccountORM(
        customer_id=customer.id,
        bank_id=bank.id,
        account_number=account_number,
        balance=account.balance,
    )
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return new_account
    

# Update an existing account
def update_account(account: AccountUpdate, db: Session):
    # Check if the account exists
    existing_account = db.query(AccountORM).filter(AccountORM.id == account.id).first()
    if not existing_account:
        raise NotFoundError("Account not found")
    
    # Case
    customer = None
    bank = None
    
    # Check if the customer exists
    if account.full_name:
        customer = db.query(CustomerORM).filter(CustomerORM.full_name == account.full_name).first()
        if not customer:
            raise NotFoundError("Customer not found")
    
    # Check if the bank exists
    if account.bank_name:
        bank = db.query(BankORM).filter(BankORM.name == account.bank_name).first()
        if not bank:
            raise NotFoundError("Bank not found")

    # Check if the account number needs to be updated
    if account.bank_name and bank.id != existing_account.bank_id:
        # Generate a unique account number based on the bank's account number validity pattern
        pattern = bank.account_number_validity_pattern
        while True:
            # Replace placeholders in the pattern with random digits
            new_account_number = re.sub(r'\[0-9\]\{(\d+)\}', 
                            lambda x: ''.join(random.choices('0123456789', k=int(x.group(1)))), 
                            pattern)
            # Check if the generated account number is unique
            existing_account_number = db.query(AccountORM).filter(AccountORM.account_number == new_account_number).first()
            if not existing_account_number:
                break
        existing_account.account_number = new_account_number

    # Update the account details
    existing_account.customer_id = customer.id if account.full_name else existing_account.customer_id
    existing_account.bank_id = bank.id if account.bank_name else existing_account.bank_id
    existing_account.balance = account.balance if account.balance else existing_account.balance

    existing_account.updated_at = datetime.now()
    
    db.commit()
    db.refresh(existing_account)
    
    return existing_account

# Get customer details by ID
def get_account_details_by_id(account_id: int, db: Session):
    account = db.query(AccountORM).filter(AccountORM.id == account_id).first()
    if not account:
        raise NotFoundError("account not found")
    
    return account
    
# Get customer details by account number
def get_account_details_by_account_number(account_number: str, db: Session):
    account = db.query(AccountORM).filter(AccountORM.account_number == account_number).first()
    if not account:
        raise NotFoundError("account not found")
    
    return account
    
# Get all accounts for a customer
def get_all_accounts_by_customer_id(customer_id: int, db: Session):
    accounts = db.query(AccountORM).filter(AccountORM.customer_id == customer_id).all()
    if not accounts:
        raise NotFoundError("No accounts found for this customer")
    
    return accounts
    
# Delete an account
def delete_account(account_id: int, db: Session):
    account = db.query(AccountORM).filter(AccountORM.id == account_id).first()
    if not account:
        raise NotFoundError("Account not found")
    
    db.delete(account)
    db.commit()
    
    return {"message": "Account deleted successfully"}