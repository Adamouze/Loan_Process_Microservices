from sqlalchemy.orm import Session
from app.orm.orm import BankingTransaction as BankingTransactionORM, Account as AccountORM
from app.models.banking_transaction import BankingTransactionCreate, TransactionType
from app.error_handling.error_types import NotFoundError, InsufficientFundsError
from datetime import datetime


# Create a new banking transaction
def create_banking_transaction(banking_transaction: BankingTransactionCreate, db: Session):
    # Check if the account exists
    account = db.query(AccountORM).filter(AccountORM.account_number == banking_transaction.account_number).first()
    if not account:
        raise NotFoundError("Account not found")
    
    # Create a new transaction
    new_transaction = BankingTransactionORM(
        account_id=account.id,
        transaction_type=banking_transaction.transaction_type,
        amount=banking_transaction.amount
    )

    # Set the account up to date
    if banking_transaction.transaction_type == "deposit":
        account.balance += banking_transaction.amount
    elif banking_transaction.transaction_type == "withdrawal":
        if account.balance < banking_transaction.amount:
            raise InsufficientFundsError("Insufficient funds")
        account.balance -= banking_transaction.amount
    else:
        raise NotFoundError("Invalid transaction type")
    
    account.updated_at = datetime.now()

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction

# Get banking transaction details by transaction ID
def get_transaction_by_id(transaction_id: int, db: Session):
    transaction = db.query(BankingTransactionORM).filter(BankingTransactionORM.id == transaction_id).first()
    if not transaction:
        raise NotFoundError("Transaction not found")
    return transaction
    
# Get banking transaction by type for a specific account
def get_transactions_by_type_and_account(account_number: str, transaction_type: TransactionType, db: Session):
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


# Get banking transaction list by account number
def get_transactions_by_account_number(account_number: str, db: Session):
    # Check if the account exists
    account = db.query(AccountORM).filter(AccountORM.account_number == account_number).first()
    if not account:
        raise NotFoundError("Account not found")
    
    # Get transactions for the account
    transactions = db.query(BankingTransactionORM).filter(BankingTransactionORM.account_id == account.id).all()
    if not transactions:
        raise NotFoundError("No transactions found for this account number")
    
    return transactions