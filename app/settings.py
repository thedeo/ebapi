import os
from dotenv import load_dotenv

load_dotenv()

# Table Configuration
API_DATA_TABLE = os.getenv("API_DATA_TABLE", "ebapi-prod-data")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# AWS Credentials (if needed)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
