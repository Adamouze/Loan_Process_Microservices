import requests
import os
import re
from sqlalchemy.orm import Session
from db.database import get_db
from orm.orm import CashierCheck as CashierCheckORM, Bank as BankORM, Customer as CustomerORM, Account as AccountORM

def validate_check_service(bank_id: int, check_id: int) -> bool:
    try:
        db: Session = next(get_db())

        check = db.query(CashierCheckORM).filter(CashierCheckORM.id == check_id).first()
        bank = db.query(BankORM).filter(BankORM.id == bank_id).first()

        if not check :
            print("Chèque introuvable")
            return False
        elif not bank :
            print("Banque introuvable")
            return False

        # Print pour tester
        print(f"[DEBUG] Bank pattern: {repr(bank.cashier_check_validity_pattern)}")
        print("check_number : " + check.check_number)
        if re.fullmatch(bank.cashier_check_validity_pattern, check.check_number):
            return True
        else:          
            return False

    except Exception as e:
        print(f"Request failed: {e}")
        return False
