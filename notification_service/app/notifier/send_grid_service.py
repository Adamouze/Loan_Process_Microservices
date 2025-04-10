# using SendGrid's Python Library
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = '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'

message = Mail(
    from_email='bardocksayajinn@gmail.com',
    to_emails='louis.charollais@telecom-sudparis.eu',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    # api_key = os.environ.get('SENDGRID_API_KEY')
    # if not api_key:
    #     raise Exception("SENDGRID_API_KEY not set")
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))