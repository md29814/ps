"""
Test EmailClient
"""
import json
import unittest

from scripts.email_client import EmailClient


class TestReceiveEmail(unittest.TestCase):
    """
    TestReceiveEmail tests
    """
    def setUp(self):
        """
        Set up
        """
        with open("/project/config/config.json") as f:
            json_data = f.read()
            config = json.loads(json_data)

        self._email_client = EmailClient(
            smtp_address=config["smtp_address"],
            pop3_address=config["pop3_address"],
            smtp_port=config["smtp_port"],
            pop3_port=config["pop3_port"],
            username=config["username"],
            password=config["password"]
        )

    def test_receive_emial(self):
        """
        Receive emial
        """
        self._email_client.receive_email()
