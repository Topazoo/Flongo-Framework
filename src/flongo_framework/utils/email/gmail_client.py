from ...config.settings import App_Settings, GMail_Settings
from gmail_python_client import GmailClient
from typing import Optional

class Gmail_Client(GmailClient):
    def __init__(self, settings:Optional[GMail_Settings]=None) -> None:
        gmail_settings = settings or App_Settings().gmail
        super().__init__(
            gmail_settings.sender_email_address,
            gmail_settings.refresh_token,
            gmail_settings.client_id,
            gmail_settings.client_secret
        )