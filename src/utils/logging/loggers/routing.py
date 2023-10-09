from src.config.enums.log_groups import LOG_GROUPS
from src.utils.logging.logging_util import LoggingUtil

class RoutingLogger(LoggingUtil):
    ''' Logger class for routes and route handling '''

    LOGGER_NAME = LOG_GROUPS.ROUTING