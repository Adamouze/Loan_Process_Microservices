from sqlalchemy.orm import Session
from app.orm.orm import Customer as CustomerORM, Account as AccountORM
from app.error_handling.error_types import NotFoundError, DBError

# Get customer details by ID
def get_account_details_by_id(account_id: int, db: Session):
    try:
        account = db.query(AccountORM).filter(AccountORM.id == account_id).first()
        if not account:
            raise NotFoundError("account not found")
        
        return account
    
    except Exception as e:
        raise DBError("Internal DB Server Error") from e
    
# Get customer details by account number
def get_account_details_by_account_number(account_number: str, db: Session):
    try:
        account = db.query(AccountORM).filter(AccountORM.account_number == account_number).first()
        if not account:
            raise NotFoundError("account not found")
        
        return account
    
    except Exception as e:
        raise DBError("Internal DB Server Error") from e
    
