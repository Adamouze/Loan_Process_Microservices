from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

# Bank table
class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    cashier_check_validity_pattern = Column(String(100), unique=True, nullable=False)

# Cashier_Check table
class CashierCheck(Base):
    __tablename__ = "cashier_check"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    check_number = Column(String(50), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    amount = Column(DECIMAL(15, 3), nullable=False)
    is_valid = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.now)