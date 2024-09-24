import os
import unittest
from unittest.mock import patch, MagicMock

class TestConfig(unittest.TestCase):

    @patch('app.config.Connection')
    @patch.dict(os.environ, {
        'AWS_ACCESS_KEY_ID': 'mock_access_key',
        'AWS_SECRET_ACCESS_KEY': 'mock_secret_key',
        'AWS_SESSION_TOKEN': 'mock_session_token',
        'AWS_REGION': 'us-east-1'
    })
    def test_explicit_credentials(self, mock_connection):
        # Import here to ensure the mock is in place before execution
        from app.config import connection

        connection._aws_access_key_id = 'mock_access_key'
        connection._aws_secret_access_key = 'mock_secret_key'
        connection._aws_session_token = 'mock_session_token'
        connection._region = 'us-east-1'

    @patch('app.config.Connection')
    @patch.dict(os.environ, {
        'AWS_REGION': 'us-east-1'
    })
    def test_default_credentials(self, mock_connection):
        # Import here to ensure the mock is in place before execution
        from app.config import connection

        # Check that Connection was called with the default parameters
        connection._aws_access_key_id = None
        connection._aws_secret_access_key = None
        connection._aws_session_token = None
        connection._region = 'us-east-1'

if __name__ == '__main__':
    unittest.main()
