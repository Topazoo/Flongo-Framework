from decimal import Decimal

from flask import current_app, has_app_context
from ...config.enums.logs.log_levels import LOG_LEVELS
from ...config.settings.base import Settings
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Sentry_Settings(Settings):
    ''' 
        Class that holds the Sentry logging configurations for the application
    '''

    GROUP_NAME = 'Sentry'

    dsn: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "SENTRY_DSN", 
            data_type=str,
            default_value=""
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    traces_sample_rate: Optional[Decimal] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "SENTRY_TRACES_SAMPLE_RATE", 
            data_type=Decimal,
            default_value="1.0"
        ),
    ) # type: ignore

    profiles_sample_rate: Optional[Decimal] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "SENTRY_PROFILES_SAMPLE_RATE", 
            data_type=Decimal,
            default_value="1.0"
        ),
    ) # type: ignore


    @classmethod
    def get_settings_from_flask(cls) -> Optional["Sentry_Settings"]:
        ''' Get the JWT settings for the current Flask app '''

        if has_app_context():
            current_settings = current_app.config.get(cls.FLASK_SETTINGS_KEY)
            if current_settings:
                return current_settings.sentry
