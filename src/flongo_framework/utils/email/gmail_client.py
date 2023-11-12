from ...config.settings import App_Settings, GMail_Settings
from gmail_python_client import GmailClient
from typing import Optional

class Gmail_Client(GmailClient):
    def __init__(self, settings:Optional[GMail_Settings]=None) -> None:
        gmail_settings = settings or App_Settings().gmail
        super().__init__(
            sender_email_address=gmail_settings.sender_email_address,
            refresh_token=gmail_settings.refresh_token,
            client_id=gmail_settings.client_id,
            client_secret=gmail_settings.client_secret
        )