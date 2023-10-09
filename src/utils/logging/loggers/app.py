from src.config.enums.log_groups import LOG_GROUPS
from src.utils.logging.logging_util import LoggingUtil

class ApplicationLogger(LoggingUtil):
    ''' Logger class for the application '''

    LOGGER_NAME = LOG_GROUPS.APP