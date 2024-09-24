'''
This file is used to set up the PynamoDB connection options.
It reads the AWS credentials from the environment variables
'''

from pynamodb.connection import Connection
from app.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION

# Set up PynamoDB connection options
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    # Use explicit credentials if they are provided
    connection = Connection(
        region=AWS_REGION,
        host=None,  # Use default DynamoDB host
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    print("Using explicit AWS credentials")
else:
    connection = Connection(region=AWS_REGION)
    print("Using instance profile or default credentials")
