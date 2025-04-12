from fastapi import FastAPI
from routes import check_validation
import uvicorn
import os

CHECK_PORT = int(os.getenv("CHECK_PORT"))

if not CHECK_PORT or CHECK_PORT <= 0:
    raise ValueError("CHECK_PORT environment variable not set.")

# FastAPI app initialization
app = FastAPI()

# Include all routers
app.include_router(check_validation.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=CHECK_PORT)
