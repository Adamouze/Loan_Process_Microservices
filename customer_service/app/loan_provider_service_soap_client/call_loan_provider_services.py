from zeep import Client
import os
from decimal import Decimal

# Load environment variables
LOAN_PROVIDER_PORT = os.getenv("LOAN_PROVIDER_PORT")

if not LOAN_PROVIDER_PORT:
    raise ValueError("LOAN_PROVIDER_PORT environment variable is not set.")

# Using the Docker service name for internal communication
wsdl_url = f"http://loan_provider_service:{LOAN_PROVIDER_PORT}/?wsdl"

Soap_client = Client(wsdl=wsdl_url)

def transfer_funds(account_id: int, amount: Decimal):
    response = Soap_client.service.transfer_funds(account_id, amount)
    return response






