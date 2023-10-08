from src.config.config import Config
from dataclasses import dataclass, field
from typing import Optional

from src.config.enums.log_levels import LOG_LEVELS

@dataclass
class FlaskConfig(Config):
    ''' 
        Class that holds the Flask application configuration
    '''

    GROUP_NAME = 'Flask'

    app_port: Optional[bool] = field(
        default_factory=lambda: Config.read_config_from_env_or_default(
            "APP_PORT", 
            data_type=int,
            default_value="2000"
        ),
    ) # type: ignore

    enable_cors: Optional[bool] = field(
        default_factory=lambda: Config.read_config_from_env_or_default(
            "APP_ENABLE_CORS", 
            data_type=bool,
            default_value="False"
        ),
    ) # type: ignore
