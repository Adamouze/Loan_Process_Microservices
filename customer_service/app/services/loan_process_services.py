from sqlalchemy.orm import Session
from app.models import *
from app.orm.orm import *
from app.risk_service_grpc_client.call_risk_services import evaluate_risk
from app.loan_provider_service_soap_client.call_loan_provider_services import transfer_funds
from app.models.loan_application_and_monitoring import Loan_ApplicationCreate, Loan_Application_with_MonitoringResponse, Loan_ApplicationResponse, LoanMonitoringResponse
from app.orm.orm import LoanApplication as Loan_ApplicationORM, LoanMonitoring as LoanMonitoringORM
from app.services.loan_application_and_monotoring_services import create_loan_application_with_monitoring
from app.error_handling.error_types import NotFoundError

def loan_process_service_first_part(loan_application: Loan_ApplicationCreate, db: Session):
    """
    First part of Loan Process Service:
    1. Create a loan application record and monoitoring record.
    2. Call risk service.
    3. Call notification service to notify the customer that he needs to submit a cashier's check.
    3.5. Call notification service to notify the customer the case of loan rejection because of risk.
    """
    # Create a loan application with monitoring record
    loan_application_and_monitoring_record = create_loan_application_with_monitoring(loan_application, db)

    loan_application_record = db.query(Loan_ApplicationORM).filter_by(id=loan_application_and_monitoring_record.Loan_Application.id).first()
    if not loan_application_record:
        raise NotFoundError("Loan application not found")
    
    loan_monitoring_record = db.query(LoanMonitoringORM).filter_by(id=loan_application_and_monitoring_record.Loan_Monitoring.id).first()
    if not loan_monitoring_record:
        raise NotFoundError("Loan monitoring record not found")

    # Call risk service
    risk_service_response = evaluate_risk(loan_application_record.account_id, loan_application.loan_amount)

    if risk_service_response.loan_status == "rejected":
        # Update loan application and monitoring status to rejected
        loan_application_record.status = "rejected"
        loan_monitoring_record.risk_status = f"risk_status : {risk_service_response.loan_status} // risk : {risk_service_response.risk_status} // reason : {risk_service_response.reason}"
        loan_monitoring_record.check_validation_status = "rejected"
        loan_monitoring_record.loan_provider_status = "rejected"
        loan_monitoring_record.notification_status = "rejected"
        loan_monitoring_record.customer_status = "rejected"
        db.commit()
        db.refresh(loan_application_record)
        db.refresh(loan_monitoring_record)
        # Call notification service to notify the customer about loan rejection
        # TODO
        # (not implemented in this snippet)
        pass
    elif risk_service_response.loan_status == "accepted":
        # Update loan applicatiton monitoring risk status to accepted":
        loan_monitoring_record.risk_status = f"risk_status : {risk_service_response.loan_status} // risk : {risk_service_response.risk_status} // reason : {risk_service_response.reason}"
        db.commit()
        db.refresh(loan_application_record)
        db.refresh(loan_monitoring_record)
        # Call notification service to notify the customer about loan approval
        # TODO
        # (not implemented in this snippet)
        pass
    else:
        # Handle other statuses as needed
        pass

    return Loan_Application_with_MonitoringResponse(
        Loan_Application=loan_application_record,
        Loan_Monitoring=loan_monitoring_record
    )
