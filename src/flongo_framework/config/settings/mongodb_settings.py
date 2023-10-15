from flask import current_app, has_app_context
from ...config.enums.logs.log_levels import LOG_LEVELS
from ...config.settings.base import Settings
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MongoDB_Settings(Settings):
    ''' 
        Class that holds the MongoDB application configuration
    '''

    GROUP_NAME = 'MongoDB'

    host: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_HOST", 
            data_type=str,
            default_value="localhost"
        ),
    ) # type: ignore

    port: Optional[int] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_PORT", 
            data_type=int,
            default_value="27017"
        ),
    ) # type: ignore

    username: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_USERNAME", 
            data_type=str,
            default_value=""
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    password: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_PASSWORD", 
            data_type=str,
            default_value=""
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    default_database: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_DEFAULT_DATABASE", 
            data_type=str,
            default_value="db"
        ),
    ) # type: ignore

    connection_timeout_ms: Optional[int] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_CONNECTION_TIMEOUT", 
            data_type=int,
            default_value="5000"
        ),
    ) # type: ignore

    log_level: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_LOG_LEVEL", 
            data_type=str,
            default_value=LOG_LEVELS.WARN
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    @classmethod
    def get_settings_from_flask(cls) -> Optional["MongoDB_Settings"]:
        ''' Get the MongoDB settings for the current Flask app '''

        if has_app_context():
            current_settings = current_app.config.get(cls.FLASK_SETTINGS_KEY)
            if current_settings:
                return current_settings.mongodb
