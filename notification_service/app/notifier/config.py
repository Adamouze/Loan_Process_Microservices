import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")