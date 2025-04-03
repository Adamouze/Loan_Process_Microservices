from fastapi import FastAPI
import uvicorn
import os
from .routes import index, accounts, banks, transactions, cashier_checks, loan_applications

CUSTOMER_SERVICE_PORT = int(os.getenv("CUSTOMER_PORT", 8000))

# FastAPI app initialization
app = FastAPI(
    title="Customer Service REST API",
    description="API for managing customers, accounts, banking transactions, loans, and checks",
    version="1.0.0"
)

# Include all routers
app.include_router(index.router)
app.include_router(accounts.router)
app.include_router(banks.router)
app.include_router(transactions.router)
app.include_router(cashier_checks.router)
app.include_router(loan_applications.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=CUSTOMER_SERVICE_PORT)