from src.config.enums.log_groups import LOG_GROUPS
from src.utils.logging.logging_util import LoggingUtil

class ApplicationConfigLogger(LoggingUtil):
    ''' Logger class for the application config '''

    LOGGER_NAME = LOG_GROUPS.APP_CONFIG