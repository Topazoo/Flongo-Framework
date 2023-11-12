from flask import current_app, has_app_context
from ..enums.logs.log_levels import LOG_LEVELS
from .base import Settings
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GMail_Settings(Settings):
    ''' 
        Class that holds the GMail configuration for the application
    '''

    GROUP_NAME = 'GMail'

    sender_email_address: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "GMAIL_SENDER_EMAIL_ADDRESS", 
            data_type=str,
            default_value="pswanson@ucdavis.edu"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    refresh_token: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "GMAIL_OAUTH_REFRESH_TOKEN", 
            data_type=str,
            default_value=""
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    client_id: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "GMAIL_OAUTH_CLIENT_ID", 
            data_type=str,
            default_value=""
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    client_secret: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "GMAIL_OAUTH_CLIENT_SECRET", 
            data_type=str,
            default_value=""
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    @classmethod
    def get_settings_from_flask(cls) -> Optional["GMail_Settings"]:
        ''' Get the GMail settings for the current Flask app '''

        if has_app_context():
            current_settings = current_app.config.get(cls.FLASK_SETTINGS_KEY)
            if current_settings:
                return current_settings.gmail
