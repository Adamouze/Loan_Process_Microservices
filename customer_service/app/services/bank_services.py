from sqlalchemy.orm import Session
from app.orm.orm import Bank as BankORM
from app.error_handling.error_types import NotFoundError

# Get bank details by ID
def get_bank_details_by_id(bank_id: int, db: Session):
    bank = db.query(BankORM).filter(BankORM.id == bank_id).first()
    if not bank:
        raise NotFoundError("Bank not found")
    
    return bank
    
# Get bank details by name
def get_bank_details_by_name(bank_name: str, db: Session):
    bank = db.query(BankORM).filter(BankORM.name == bank_name).first()
    if not bank:
        raise NotFoundError("Bank not found")
    
    return bank
    
# Get all banks
def get_all_banks(db: Session):
    banks = db.query(BankORM).all()
    if not banks:
        raise NotFoundError("No banks found")
    
    return banks