from src.config.enums.logs.log_groups import LOG_GROUPS
from src.utils.logging.logging_util import LoggingUtil

class DatabaseLogger(LoggingUtil):
    ''' Logger class for the database '''

    LOGGER_NAME = LOG_GROUPS.DATABASE