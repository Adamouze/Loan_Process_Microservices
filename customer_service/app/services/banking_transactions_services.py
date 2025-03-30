from sqlalchemy.orm import Session
from app.orm.orm import BankingTransaction as BankingTransactionORM, Account as AccountORM
from app.error_handling.error_types import NotFoundError, DBError

# Get banking transaction details by transaction ID
def get_transaction_by_id(transaction_id: int, db: Session):
    try:
        transaction = db.query(BankingTransactionORM).filter(BankingTransactionORM.id == transaction_id).first()
        if not transaction:
            raise NotFoundError("Transaction not found")
        return transaction
    except Exception as e:
        raise DBError("Internal DB Server Error") from e
    
# Get banking transaction by type for a specific account
def get_transactions_by_type_and_account(account_number: str, transaction_type: str, db: Session):
    try:
        # Check if the account exists
        account = db.query(AccountORM).filter(AccountORM.account_number == account_number).first()
        if not account:
            raise NotFoundError("Account not found")
        
        # Get transactions for the account and type
        transactions = db.query(BankingTransactionORM).filter(
            BankingTransactionORM.account_id == account.id,
            BankingTransactionORM.transaction_type == transaction_type
        ).all()
        
        if not transactions:
            raise NotFoundError("No transactions found for this account number and type")
        
        return transactions
    except Exception as e:
        raise DBError("Internal DB Server Error") from e


# Get banking transaction list by account number
def get_transactions_by_account_number(account_number: str, db: Session):
    try:
        # Check if the account exists
        account = db.query(AccountORM).filter(AccountORM.account_number == account_number).first()
        if not account:
            raise NotFoundError("Account not found")
        
        # Get transactions for the account
        transactions = db.query(BankingTransactionORM).filter(BankingTransactionORM.account_id == account.id).all()
        if not transactions:
            raise NotFoundError("No transactions found for this account number")
        
        return transactions
    except Exception as e:
        raise DBError("Internal DB Server Error") from e