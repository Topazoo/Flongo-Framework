import logging
from ....config.enums.base.base_str_enum import BaseStrEnum

class LOG_LEVELS(BaseStrEnum):
    """ Log levels supported by the application """

    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"

    @staticmethod
    def level_to_int(log_level:str) -> int:
        if log_level == LOG_LEVELS.DEBUG:
            return logging.DEBUG
        if log_level == LOG_LEVELS.INFO:
            return logging.INFO
        if log_level == LOG_LEVELS.WARN:
            return logging.WARN
        if log_level == LOG_LEVELS.ERROR:
            return logging.ERROR
        if log_level == LOG_LEVELS.CRITICAL:
            return logging.CRITICAL
        
        return logging.FATAL
