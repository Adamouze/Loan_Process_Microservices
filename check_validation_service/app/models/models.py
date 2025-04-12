from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CashierCheck(Base):
    __tablename__ = "cashier_check"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    check_number = Column(String)
    issue_date = Column(DateTime)
    amount = Column(Integer)
    is_valid = Column(Boolean)
    created_at = Column(DateTime)

class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cashier_check_validity_pattern = Column(String)
