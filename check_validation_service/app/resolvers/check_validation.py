from db.database import get_db
from sqlalchemy.orm import Session
from models.models import CashierCheck, Bank
import re

def validate_check_resolver(bank_id: int, check_id: int) -> bool:
    db: Session = next(get_db())

    check = db.query(CashierCheck).filter(CashierCheck.id == check_id).first()
    if not check:
        return False

    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        return False

    # Vérification : le chèque est marqué comme valide et respecte le pattern de la banque
    pattern = bank.cashier_check_validity_pattern
    if not re.fullmatch(pattern, check.check_number):
        return False

    return check.is_valid
