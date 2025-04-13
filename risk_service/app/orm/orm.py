from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from ..db.database import Base
from datetime import datetime

# Account table
class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), unique=True, nullable=False)
    balance = Column(DECIMAL(15, 2), nullable=False, default=0)
    created_at = Column(DateTime, nullable=True, default=datetime.now, onupdate=None)
    updated_at = Column(DateTime, nullable=True, default=datetime.now)

    # Relationships
    banking_transactions = relationship("BankingTransaction", backref="account", cascade="all, delete-orphan")

# Banking transaction table
class BankingTransaction(Base):
    __tablename__ = "banking_transaction"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    transaction_date = Column(DateTime, nullable=True, default=datetime.now)