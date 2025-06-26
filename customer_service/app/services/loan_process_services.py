from sqlalchemy.orm import Session
from sqlalchemy.orm.session import object_session

from app.models.notification import MessageType

from app.services.customer_services import get_customer_by_id
from app.services.account_services import get_account_details_by_id, get_account_details_by_account_number

from app.notification_service_client.call_notification_service import send_notification_service
from app.risk_service_grpc_client.call_risk_services import evaluate_risk
from app.check_validation_service_graphql_client.call_check_validation_service import validate_check_service
from app.loan_provider_service_soap_client.call_loan_provider_services import transfer_funds

from app.services.cashier_check_services import submit_cashier_check

from app.services.loan_application_and_monotoring_services import create_loan_application_with_monitoring, get_loan_application_with_monitoring

from app.models.loan_application_and_monitoring import Loan_ApplicationCreate, Loan_Application_with_MonitoringResponse, Loan_ApplicationResponse, LoanMonitoringResponse
from app.models.notification import NotificationRequest
from app.models.cashier_check import CashierCheckCreate

from app.error_handling.error_types import NotFoundError

MAX_LOAN_AMOUNT = 1000000  # Maximum loan amount allowed

def loan_process_service_first_part(loan_application: Loan_ApplicationCreate, db: Session):
    """
    First part of Loan Process Service:
    1. Create a loan application record and monoitoring record;
    2. Check if the loan amount is greater than the maximum allowed amount.
    3. Call risk service.
    4. Call notification service to notify the customer that he needs to submit a cashier's check.
    4.5. Call notification service to notify the customer the case of loan rejection because of risk.
    """

    # Create a loan application with monitoring record
    loan_application_and_monitoring_record = create_loan_application_with_monitoring(loan_application, db)

    if not loan_application_and_monitoring_record:
        raise NotFoundError("Loan application with monitoring record not found")
    
    loan_application_record = loan_application_and_monitoring_record["Loan_Application"]
    loan_monitoring_record = loan_application_and_monitoring_record["Loan_Monitoring"]
    
    if not loan_application_record or not loan_monitoring_record:
        raise NotFoundError("Loan application or monitoring record not found")

    # Instantiate the message type for notification service
    messages = MessageType()

    # Get customer_id from loan application record
    account_id = loan_application_record.account_id

    # Get customer_id from account_id
    customer_id = get_account_details_by_id(account_id, db).customer_id

    # Get customer email from customer_id
    customer_email = get_customer_by_id(customer_id, db).email
    
    if loan_application_record.loan_amount > MAX_LOAN_AMOUNT:
        loan_application_record.status = "rejected"
        loan_monitoring_record.risk_status = "rejected"
        loan_monitoring_record.check_validation_status = "rejected"
        loan_monitoring_record.loan_provider_status = "rejected"
        loan_monitoring_record.customer_status = f"Requested amount: {loan_application.loan_amount}, Maximum allowed: {MAX_LOAN_AMOUNT}"
        db.commit()
        db.refresh(loan_application_record)
        db.refresh(loan_monitoring_record)

        # Prepare the notification message
        html_email = messages.get_email_content(
            "Loan_Application_Maximum_Amount_Achieved",
            custom_message=f"Requested amount: {loan_application.loan_amount}, Maximum allowed: {MAX_LOAN_AMOUNT}"
        )
        
        # Send notification to the customer
        send_notification_response = send_notification_service(
            NotificationRequest(
                receiver_address=customer_email,
                message=html_email
            )
        )

        if not send_notification_response.status:
            loan_monitoring_record.notification_status = "failed"
            loan_monitoring_record.customer_status = "rejected"
            db.commit()
            db.refresh(loan_monitoring_record)
            raise Exception("Failed to send notification")
        else:
            # Update notification status in loan monitoring record
            loan_monitoring_record.notification_status = "notified"
            db.commit()
            db.refresh(loan_monitoring_record)

        return Loan_Application_with_MonitoringResponse(
            Loan_Application=Loan_ApplicationResponse.model_validate(loan_application_record),
            Loan_Monitoring=LoanMonitoringResponse.model_validate(loan_monitoring_record)
        )

    elif loan_application_record.loan_amount <= MAX_LOAN_AMOUNT:
        # Call risk service
        risk_service_response = evaluate_risk(loan_application_record.account_id, loan_application.loan_amount)
    else:
        raise Exception("Invalid loan amount")

    if risk_service_response.loan_status == "rejected":
        # Update loan application and monitoring status to rejected
        loan_application_record.status = "rejected"
        loan_monitoring_record.risk_status = f"loan_status : {risk_service_response.loan_status} // risk : {risk_service_response.risk_status} // reason : {risk_service_response.reason}"
        loan_monitoring_record.check_validation_status = "rejected"
        loan_monitoring_record.loan_provider_status = "rejected"
        loan_monitoring_record.notification_status = "rejected"
        loan_monitoring_record.customer_status = "rejected"
        db.commit()
        db.refresh(loan_application_record)
        db.refresh(loan_monitoring_record)

        # Call notification service to notify the customer about loan rejection
        html_email = messages.get_email_content(
            "Risk_Service_Rejected",
            custom_message=loan_monitoring_record.risk_status
        )

        send_notification_response = send_notification_service(
            NotificationRequest(
                receiver_address=customer_email,
                message=html_email
            )
        )

        if not send_notification_response.status:
            loan_monitoring_record.notification_status = "failed"
            loan_monitoring_record.customer_status = "rejected"
            db.commit()
            db.refresh(loan_monitoring_record)
            raise Exception("Failed to send notification")
        else:
            # Update notification status in loan monitoring record
            loan_monitoring_record.notification_status = "notified"
            db.commit()
            db.refresh(loan_monitoring_record)

    elif risk_service_response.loan_status == "accepted":
        # Update loan applicatiton monitoring risk status to accepted":
        loan_monitoring_record.risk_status = f"risk_status : {risk_service_response.loan_status} // risk : {risk_service_response.risk_status} // reason : {risk_service_response.reason}"
        db.commit()
        db.refresh(loan_application_record)
        db.refresh(loan_monitoring_record)
        # Call notification service to notify the customer about loan approval
        html_email = messages.get_email_content(
            "Risk_Service_Accepted",
            custom_message=f"{loan_monitoring_record.risk_status}<br><br><strong>Here is your loan application id: {loan_application_record.id}</strong>"
        )

        send_notification_response = send_notification_service(
            NotificationRequest(
                receiver_address=customer_email,
                message=html_email
            )
        )

        if send_notification_response.status != True:
            loan_monitoring_record.customer_status = "rejected"
            loan_monitoring_record.notification_status = "failed"
            db.commit()
            db.refresh(loan_monitoring_record)
            raise Exception("Failed to send notification")
        else:
            # Update notification status in loan monitoring record
            loan_monitoring_record.notification_status = "notified"
            db.commit()
            db.refresh(loan_monitoring_record)
    else:
        # Raise an exception if the loan status is not accepted or rejected
        raise Exception("Invalid loan status")

    return Loan_Application_with_MonitoringResponse(
        Loan_Application=Loan_ApplicationResponse.model_validate(loan_application_record),
        Loan_Monitoring=LoanMonitoringResponse.model_validate(loan_monitoring_record)
    )

def loan_process_service_second_part(loan_application_id : int, cashier_check: CashierCheckCreate, db: Session):
    """
    Second part of Loan Process Service:
    1. Call check validation service to validate cashier's check.
    2. Call notification service to notify the customer about cashier's check validation in a case of failure.
    3. Call loan provider service to transfer funds.
    4. Call notification service to notify the customer about funds transfer.
    """

    # Get loan application and monitoring records
    loan_application_and_monitoring_record = get_loan_application_with_monitoring(loan_application_id, db)

    if not loan_application_and_monitoring_record:
        raise NotFoundError("Loan application with monitoring record not found")

    loan_application_record = loan_application_and_monitoring_record["Loan_Application"]
    loan_monitoring_record = loan_application_and_monitoring_record["Loan_Monitoring"]

    if not loan_application_record or not loan_monitoring_record:
        raise NotFoundError("Loan application or monitoring record not found")

    # Instantiate the message type for notification service
    messages = MessageType()

    # Get account_number from cashier check record
    account_number = cashier_check.account_number

    # Get customer_details from account_number
    account_details = get_account_details_by_account_number(account_number, db)

    # Get account_id from account_number
    account_id = account_details.id

    # Get customer_id from account_number
    customer_id = account_details.customer_id

    # Get bank_id from account_number
    bank_id = account_details.bank_id

    # Get customer email from customer_id
    customer_email = get_customer_by_id(customer_id, db).email

    # Verify if the account_number of the cashier check is the same as the one in the loan application
    if account_id != loan_application_record.account_id:
        raise NotFoundError("Account number mismatch between cashier check and loan application")

    # Call check validation service to validate cashier's check
    check_validation_response = validate_check_service(bank_id, cashier_check.check_number)

    if (check_validation_response == True) or (check_validation_response == False):
        # Submit cashier check to the bank account
        submit_check = CashierCheckCreate(
            account_number=account_number,
            check_number=cashier_check.check_number,
            issue_date=cashier_check.issue_date,
            amount=cashier_check.amount,
            is_valid=check_validation_response
        )

        submitted_check = submit_cashier_check(submit_check, db)

        if not submitted_check.id:
            raise NotFoundError("Submitted Cashier check not found")

    if check_validation_response == False:
        # Update loan application and monitoring status to rejected
        loan_application_record.status = "rejected"
        loan_monitoring_record.check_validation_status = f"check_status : {check_validation_response}"
        loan_monitoring_record.loan_provider_status = "rejected"
        loan_monitoring_record.customer_status = "rejected"
        db.commit()
        db.refresh(loan_application_record)
        db.refresh(loan_monitoring_record)

        # Call notification service to notify the customer about cashier's check validation failure
        html_email = messages.get_email_content(
            "Check_Validation_Rejected",
            custom_message=loan_monitoring_record.check_validation_status
        )

        send_notification_response = send_notification_service(
            NotificationRequest(
                receiver_address=customer_email,
                message=html_email
            )
        )

        if not send_notification_response.status:
            loan_monitoring_record.notification_status = "failed"
            loan_monitoring_record.customer_status = "rejected"
            db.commit()
            db.refresh(loan_monitoring_record)
            raise Exception("Failed to send notification")
        else:
            # Update notification status in loan monitoring record
            loan_monitoring_record.notification_status = "notified"
            db.commit()
            db.refresh(loan_monitoring_record)

    elif check_validation_response == True:
        # Update loan application and monitoring status to reflect successful check validation
        loan_monitoring_record.check_validation_status = f"check_status : {check_validation_response}"
        db.commit()
        db.refresh(loan_application_record)
        db.refresh(loan_monitoring_record)

        # Call loan provider service to transfer funds
        transfer_funds_response = transfer_funds(account_id, loan_application_record.loan_amount)

        if "approved" in transfer_funds_response:
            # Update loan application and monitoring status to reflect successful fund transfer
            loan_application_record.status = "approved"
            loan_monitoring_record.loan_provider_status = f"{transfer_funds_response}"
            loan_monitoring_record.customer_status = "approved"
            db.commit()
            db.refresh(loan_application_record)
            db.refresh(loan_monitoring_record)

            # Call notification service to notify the customer about successful fund transfer
            html_email = messages.get_email_content(
                "Loan_Provided",
                custom_message=f"<strong>{transfer_funds_response}</strong>"
            )

            send_notification_response = send_notification_service(
                NotificationRequest(
                    receiver_address=customer_email,
                    message=html_email
                )
            )

            if not send_notification_response.status:
                loan_monitoring_record.notification_status = "failed"
                loan_monitoring_record.customer_status = "rejected"
                db.commit()
                db.refresh(loan_monitoring_record)
                raise Exception("Failed to send notification")
            else:
                # Update notification status in loan monitoring record
                loan_monitoring_record.notification_status = "notified"
                db.commit()
                db.refresh(loan_monitoring_record)
        else:
            # Handle fund transfer failure
            loan_monitoring_record.loan_provider_status = "transfer_failed"
            loan_monitoring_record.customer_status = "rejected"
            db.commit()
            db.refresh(loan_monitoring_record)
            raise Exception("Fund transfer failed")
    else:
        # Raise an exception if the check validation status is not accepted or rejected
        raise Exception("Invalid check validation status")

    return Loan_Application_with_MonitoringResponse(
        Loan_Application=Loan_ApplicationResponse.model_validate(loan_application_record),
        Loan_Monitoring=LoanMonitoringResponse.model_validate(loan_monitoring_record)
    )
