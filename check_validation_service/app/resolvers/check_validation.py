from db.database import get_db
from sqlalchemy.orm import Session
from orm.orm import Bank
import re

def validate_check_resolver(bank_id: int, check_number: str) -> bool:
    db: Session = next(get_db())

    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise Exception("Banque introuvable")

    # Verification of the check number format
    pattern = bank.cashier_check_validity_pattern
    if not re.fullmatch(pattern, check_number):
        return False

    return True
