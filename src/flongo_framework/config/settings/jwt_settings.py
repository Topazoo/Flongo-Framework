from flask import current_app, has_app_context
from ...config.enums.logs.log_levels import LOG_LEVELS
from ...config.settings.base import Settings
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class JWT_Settings(Settings):
    ''' 
        Class that holds the JSON Web Token (JWT) configuration for the application
    '''

    GROUP_NAME = 'JWT'

    secret_key: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "JWT_SECRET_KEY", 
            data_type=str,
            default_value="Change me!"
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    password_salt: Optional[bytes] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "JWT_PASSWORD_SALT", 
            data_type=bytes,
            default_value='$2b$12$eSed7n6el5ZZRIKusxMqWu'
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    access_token_expiration_secs: Optional[int] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "JWT_ACCESS_TOKEN_EXPIRATION_SECS", 
            data_type=int,
            default_value="300"
        ),
    ) # type: ignore

    refresh_access_token_within_secs: Optional[int] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "JWT_REFRESH_ACCESS_TOKEN_WITHIN_SECS", 
            data_type=int,
            default_value="60"
        ),
    ) # type: ignore

    refresh_token_expiration_secs: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "JWT_REFRESH_TOKEN_EXPIRATION_SECS", 
            data_type=int,
            default_value="300"
        ),
    ) # type: ignore

    only_allow_https: Optional[bool] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "JWT_ONLY_ALLOW_HTTPS", 
            data_type=bool,
            default_value="False"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    enable_csrf_protection: Optional[bool] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "JWT_ENABLE_CSRF_PROTECTION", 
            data_type=bool,
            default_value="False"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore


    @classmethod
    def get_settings_from_flask(cls) -> Optional["JWT_Settings"]:
        ''' Get the JWT settings for the current Flask app '''

        if has_app_context():
            current_settings = current_app.config.get(cls.FLASK_SETTINGS_KEY)
            if current_settings:
                return current_settings.jwt
