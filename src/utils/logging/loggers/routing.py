import logging
from src.config.enums.log_colors import LOG_FOREGROUND_COLORS
from src.config.enums.log_groups import LOG_GROUPS
from src.utils.logging.logging_util import LoggingUtil

class RoutingLogger(LoggingUtil):
    ''' Logger class for routes and route handling '''

    @property
    def LOGGER_NAME(self):
        name = f"{LOG_GROUPS.ROUTING}"
        if self.url:
            name += f":[{self.url}]"
        if self.method:
            name += f":[{self.method}]"

        return name

    def __init__(self, url:str='', method:str='') -> None:
        self.url = url
        self.method = method

    def info(self, msg:str):
        ''' Emit a info log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).info, LOG_FOREGROUND_COLORS.GREEN)

    def debug(self, msg:str):
        ''' Emit a debug log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).debug, LOG_FOREGROUND_COLORS.BLUE)

    def warn(self, msg:str):
        ''' Emit a warning log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).warn, LOG_FOREGROUND_COLORS.YELLOW)

    def error(self, msg:str):
        ''' Emit an error log '''

        self._log(msg, logging.getLogger(self.LOGGER_NAME).error, LOG_FOREGROUND_COLORS.RED)

    def critical(self, msg:str):
        ''' Emit a critical error log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).critical, LOG_FOREGROUND_COLORS.PURPLE)
