from sqlalchemy.orm import Session
from app.models.loan_application import Loan_ApplicationCreate
from customer_service.app.orm.orm import LoanApplication as Loan_ApplicationORM, Customer as CustomerORM, Account as AccountORM, LoanMonitoring as LoanMonitoringORM
from error_handling.error_types import NotFoundError, DBError, LoanAmountTooHighError

MAX_LOAN_AMOUNT = 1000000  # Maximum loan amount allowed

# Create a loan application
def create_loan_application(loan_application: Loan_ApplicationCreate, db: Session):
    if loan_application.loan_amount > MAX_LOAN_AMOUNT:
        raise LoanAmountTooHighError("Loan amount exceeds the maximum limit")
    
    customer = db.query(CustomerORM).filter(CustomerORM.id == loan_application.customer_id).first()
    if not customer:
        raise NotFoundError("Customer not found")
    
    account = db.query(AccountORM).filter(AccountORM.id == loan_application.account_number).first()
    if not account:
        raise NotFoundError("Account not found")
    
    db_loan_application = Loan_ApplicationORM(
        customer_id=customer.id,
        account_id=account.id,
        loan_type=loan_application.loan_type,
        loan_amount=loan_application.loan_amount,
        loan_description=loan_application.loan_description,
        status="pending",
        email=loan_application.email
    )
    
    db.add(db_loan_application)
    db.commit()
    db.refresh(db_loan_application)
    
    return db_loan_application

# Create a loan monitoring record
def create_loan_monitoring(loan_application_id: int, db: Session):
    loan_application = db.query(Loan_ApplicationORM).filter(Loan_ApplicationORM.id == loan_application_id).first()
    if not loan_application:
        raise NotFoundError("No loan_application found with that id")
    
    loan_monitoring = LoanMonitoringORM(
        loan_application_id=loan_application.id,
        risk_status="pending",
        check_validation_status="pending",
        loan_provider_status="pending",
        notification_status="pending",
        customer_status="pending",
    )
    
    db.add(loan_monitoring)
    db.commit()
    db.refresh(loan_monitoring)
    
    return loan_monitoring

# Create a loan application with monitoring
def create_loan_application_with_monitoring(loan_application: Loan_ApplicationCreate, db: Session):
    loan_application_record = create_loan_application(loan_application, db)
    loan_monitoring_record = create_loan_monitoring(loan_application_record.id, db)
    
    return {
        "loan_application": loan_application_record,
        "loan_monitoring": loan_monitoring_record
    }

# Get a loan application by ID
def get_loan_application_by_id(loan_application_id: int, db: Session):
    try :
        loan_application = db.query(Loan_ApplicationORM).filter(Loan_ApplicationORM.id == loan_application_id).first()
        if not loan_application:
            raise NotFoundError("No loan_application found with that id")
        return loan_application
    except Exception as e:
        raise DBError("Internal DB Server Error") from e

# Get loan applications by account number  
def get_loan_applications_by_account_number(account_number: str, db: Session):
    try:
        loan_application = db.query(Loan_ApplicationORM).join(Loan_ApplicationORM.account).filter(Loan_ApplicationORM.account.account_number == account_number).all()
        if not loan_application:
            raise NotFoundError("No loan_applications found with that account number")
        return loan_application
    except Exception as e:
        raise DBError("Internal DB Server Error") from e

# Get loan applications with monitoring information
def get_loan_application_with_monitoring(loan_application_id: int, db: Session):
    loan_application = db.query(Loan_ApplicationORM).filter(Loan_ApplicationORM.id == loan_application_id).first()
    if not loan_application:
        raise NotFoundError("No loan_application found with that id")
    
    return {
        "loan_application": loan_application,
        "loan_monitoring": loan_application.loan_monitoring
    }


