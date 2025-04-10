from fastapi import FastAPI
from routes import notifier
import uvicorn
import os

NOTIFICATION_PORT = int(os.getenv("NOTIFICATION_PORT"))

if not NOTIFICATION_PORT or NOTIFICATION_PORT <= 0:
    raise ValueError("NOTIFICATION_PORT environment variable not set.")

# FastAPI app initialization
app = FastAPI()

# Include all routers
app.include_router(notifier.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=NOTIFICATION_PORT)
