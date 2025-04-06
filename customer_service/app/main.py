from fastapi import FastAPI
import uvicorn
import os
from .routes import banking_transaction, accounts, banks, cashier_checks, loan_applications, customer, loan_process
from app.error_handling.error_handler import register_error_handlers
from app.loan_provider_service_soap_client.call_loan_provider_services import transfer_funds

CUSTOMER_SERVICE_PORT = int(os.getenv("CUSTOMER_PORT"))

if not CUSTOMER_SERVICE_PORT or CUSTOMER_SERVICE_PORT <= 0:
    raise ValueError("CUSTOMER_PORT environment variable not set.")

# FastAPI app initialization
app = FastAPI(
    title="Customer Service REST API",
    description="API for managing customers, accounts, banking transactions, loans, and checks",
    version="1.0.0"
)

# Include all routers
app.include_router(customer.router)
app.include_router(accounts.router)
app.include_router(banks.router)
app.include_router(banking_transaction.router)
app.include_router(cashier_checks.router)
app.include_router(loan_applications.router)
app.include_router(loan_process.router)

# Register error handlers
register_error_handlers(app)

if __name__ == "__main__":
    # Run the app with uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=CUSTOMER_SERVICE_PORT)