from sqlalchemy import Column, Integer, String
from db.database import Base

# Bank table
class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    account_number_validity_pattern = Column(String(100), unique=True, nullable=False)
    cashier_check_validity_pattern = Column(String(100), unique=True, nullable=False)