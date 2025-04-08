from app.proto import risk_pb2, risk_pb2_grpc
from app.db.database import get_db
from app.orm.orm import Account as AccountORM, BankingTransaction as BankingTransactionORM
from sqlalchemy.orm import Session
from sqlalchemy import func

class RiskService(risk_pb2_grpc.RiskServiceServicer):

    def AnalyzeRisk(self, request, context):
        db: Session = next(get_db())

        # 1. Vérifie que le compte existe
        account = db.query(AccountORM).filter(AccountORM.id == request.account_id).first()
        if not account:
            context.abort(404, "Account not found")

        # 2. Récupère les transactions
        transactions = db.query(BankingTransactionORM).filter_by(account_id=account.id).all()
        if not transactions:
            context.abort(404, "No transactions found for this account")

        # 3. Analyse des transactions
        withdrawals = [t for t in transactions if t.transaction_type.lower() == "withdrawal"]
        withdrawal_ratio = len(withdrawals) / len(transactions)

        # 4. Solde moyen
        avg_balance = db.query(func.avg(AccountORM.balance)).filter(AccountORM.id == account.id).scalar() or 0

        # 5. Analyse de risque
        is_high_risk = withdrawal_ratio > 0.5 and avg_balance < 5000
        if is_high_risk and request.loan_amount > 20000:
            return risk_pb2.RiskResponse(
                loan_status="rejected",
                risk_status="high",
                reason="High number of withdrawals and low average balance. Loan amount too high."
            )
        else:
            return risk_pb2.RiskResponse(
                loan_status="accepted",
                risk_status="high" if is_high_risk else "low",
                reason="Loan approved based on current risk assessment."
            )
