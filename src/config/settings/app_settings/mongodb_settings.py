from src.config.enums.log_levels import LOG_LEVELS
from src.config.settings.base.base_settings import Settings
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
    ) # type: ignore

    password: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_PASSWORD", 
            data_type=str,
            default_value=""
        ),
    ) # type: ignore

    default_database: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_DEFAULT_DATABASE", 
            data_type=str,
            default_value="db"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    connection_timeout: Optional[int] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "MONGODB_CONNECTION_TIMEOUT", 
            data_type=int,
            default_value="600"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore
