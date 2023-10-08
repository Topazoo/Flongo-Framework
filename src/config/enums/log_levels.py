from src.config.enums.base.base_str_enum import BaseStrEnum

class LOG_LEVELS(BaseStrEnum):
    """ Log levels supported by the application """

    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"
