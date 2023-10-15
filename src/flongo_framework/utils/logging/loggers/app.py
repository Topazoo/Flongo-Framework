from src.flongo_framework.config.enums.logs.log_groups import LOG_GROUPS
from src.flongo_framework.utils.logging.logging_util import LoggingUtil

class ApplicationLogger(LoggingUtil):
    ''' Logger class for the application '''

    LOGGER_NAME = LOG_GROUPS.APP