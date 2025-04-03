from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from ..db.database import Base
from datetime import datetime


# Customer table
class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relationships
    accounts = relationship("Account", backref="customer", cascade="all, delete-orphan")

# Bank table
class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    cashier_check_validity_pattern = Column(String(100), unique=True, nullable=False)

    # Relationships
    accounts = relationship("Account", backref="bank", cascade="all, delete-orphan")

# Account table
class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"), nullable=False)
    bank_id = Column(Integer, ForeignKey("bank.id", ondelete="CASCADE"), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    balance = Column(DECIMAL(15, 2), nullable=False, default=0)
    created_at = Column(DateTime, nullable=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, default=datetime.now)

    # Relationships
    loan_applications = relationship("LoanApplication", backref="account", cascade="all, delete-orphan")
    cashier_checks = relationship("CashierCheck", backref="account", cascade="all, delete-orphan")
    banking_transactions = relationship("BankingTransaction", backref="account", cascade="all, delete-orphan")

# Banking transaction table
class BankingTransaction(Base):
    __tablename__ = "banking_transaction"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    transaction_date = Column(DateTime, nullable=True, default=datetime.now)

# Loan application table
class LoanApplication(Base):
    __tablename__ = "loan_application"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    loan_type = Column(String(20), nullable=False)
    loan_amount = Column(DECIMAL(15, 2), nullable=False)
    loan_description = Column(Text)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.now)

    # 1:1 Relationships
    loan_monitoring = relationship("LoanMonitoring", uselist=False, cascade="all, delete-orphan")

# Cashier_Check table
class CashierCheck(Base):
    __tablename__ = "cashier_check"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    bank_id = Column(Integer, ForeignKey("bank.id", ondelete="CASCADE"), nullable=False)
    check_number = Column(String(50), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    amount = Column(DECIMAL(15, 3), nullable=False)
    is_valid = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.now)

# Loan monitoring table
class LoanMonitoring(Base):
    __tablename__ = "loan_monitoring"

    id = Column(Integer, primary_key=True, index=True)
    loan_application_id = Column(Integer, ForeignKey("loan_application.id", ondelete="CASCADE"), nullable=False, unique=True)  # UNIQUE
    monitoring_date = Column(DateTime, nullable=True, default=datetime.now)
    risk_status = Column(String(20))
    check_validation_status = Column(String(20))
    loan_provider_status = Column(String(20))
    notification_status = Column(String(20))
    customer_status = Column(String(20))