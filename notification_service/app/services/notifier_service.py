import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models.notifier import NotificationRequest, NotificationResponse

api_key = os.environ.get('SENDGRID_API_KEY')
sender_address = os.environ.get('SENDER_ADDRESS')

if not api_key :
    raise ValueError("SENDGRID_API_KEY environment variable not set.")

if not sender_address:
    raise ValueError("SENDER_ADDRESS environment variable not set.")

def send_notification(notification: NotificationRequest) -> bool:
    mail = Mail(
        from_email = sender_address,
        to_emails = notification.receiver_address,
        subject = 'Loan Process Microservice Status',
        html_content = notification.message)
    # message du type : '<strong>and easy to do anywhere, even with Python</strong>'
    
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)
        return NotificationResponse(
            status = True if response.status_code == 202 else False
        )
    except Exception as e:
        raise e
