import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = os.environ.get('SENDGRID_API_KEY')
sender_address = os.environ.get('SENDER_ADDRESS')

def send_notification(receiver_address: str, message: str) -> int:
    mail = Mail(
        from_email = sender_address,
        to_emails = receiver_address,
        subject = 'Loan Process Microservice Status',
        html_content = message)
    # message du type : '<strong>and easy to do anywhere, even with Python</strong>'
    
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)
        return response.status_code
    except Exception as e:
        print(str(e))
