from spyne import rpc, ServiceBase, Unicode, Integer
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.orm.orm import Account as AccountORM, BankingTransaction as BankingTransactionORM
from app.error_handling.error_types import NotFoundError

class LoanProviderService(ServiceBase):
    @rpc(Integer, Integer, _returns=Unicode)
    def transfer_funds(ctx, account_id, amount):
        db: Session = next(get_db())

        # Check if the account exists
        account = db.query(AccountORM).filter(AccountORM.id == account_id).first()
        if not account:
            raise NotFoundError("Account not found")

        # Update the account balance and updated_at
        account.balance += amount
        account.updated_at = datetime.now()

        # Add a transaction record
        transaction = BankingTransactionORM(
            account_id=account.id,
            transaction_type="transfer",
            amount=amount
        )

        db.add(transaction)

        db.commit()
        db.refresh(account)

        return f"Transfer of {amount} approved for account {account_id}."