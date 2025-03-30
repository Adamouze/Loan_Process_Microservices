from app.orm.orm import CashierCheck as CashierCheckORM
from app.models.cashier_check import CashierCheckCreate
from sqlalchemy.orm import Session
from app.error_handling.error_types import NotFoundError, DBError
import requests
import os

GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT",0)

# TODO : Implement the GraphQL mutation to create and verify a cashier check
# def submit_cashier_check(cashier_check: CashierCheckCreate):
#     query = """
#     mutation CreateAndVerifyCashierCheck($input: CashierCheckInput!) {
#         createAndVerifyCashierCheck(input: $input) {
#             check_number
#             is_valid
#             message
#         }
#     }
#     """
#     variables = {
#         "input": {
#             "account_number": cashier_check.account_number,
#             "bank_name": cashier_check.bank_name,
#             "check_number": cashier_check.check_number,
#             "issue_date": cashier_check.issue_date,
#             "amount": cashier_check.amount
#         }
#     }
#     response = requests.post(GRAPHQL_ENDPOINT, json={"query": query, "variables": variables})
#     return response.json()

# def create_cashier_check(CashierCheck : CashierCheckCreate, db: Session):
#     try:
#         # Check if the account exists
#         account = db.query(AccountORM).filter(AccountORM.account_number == CashierCheck.account_number).first()
#         if not account:
#             raise NotFoundError("Account not found")
        
#         # Check if the bank exists
#         bank = db.query(BankORM).filter(BankORM.name == CashierCheck.bank_name).first()
#         if not bank:
#             raise NotFoundError("Bank not found")
        
#         cashier_check = CashierCheckORM(
#             account_number=CashierCheck.account_number,
#             bank_name=CashierCheck.bank_name,
#             check_number=CashierCheck.check_number,
#             issue_date=datetime.strptime(CashierCheck.issue_date, "%Y-%m-%d"),
#             amount=CashierCheck.amount,
#             is_valid=False, # Assuming default is invalid
#             created_at=datetime.now()
#         )
        
#         db.add(cashier_check)
#         db.commit()
#         db.refresh(cashier_check)

#         return cashier_check
    
#     except Exception as e:
#         raise DBError("Internal DB Server Error") from e

def get_cashier_check(check_number: str, db: Session):
    try:
        cashier_check = db.query(CashierCheckORM).filter(CashierCheckORM.check_number == check_number).first()
        if not cashier_check:
            raise NotFoundError("Cashier check not found")
        return cashier_check
    except Exception as e:
        raise DBError("Internal DB Server Error") from e