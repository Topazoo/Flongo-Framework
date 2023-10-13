import logging

import logging

from src.config.enums.logs.colors import LOG_TEXT_COLORS
from src.config.enums.logs.log_groups import LOG_GROUPS
from src.utils.logging.logging_util import LoggingUtil

class StatefulLoggingUtil(LoggingUtil):
    ''' Base logger class for the application with state '''

    _BASE_NAME = LOG_GROUPS.ROOT

    @property
    def LOGGER_NAME(self):
        name = f"{self._BASE_NAME}"
        if self.name:
            name += f":[{self.name}]"

        return name

    def __init__(self, name:str='') -> None:
        self.name = name

    def info(self, msg:str):
        ''' Emit a info log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).info, LOG_TEXT_COLORS.GREEN)

    def debug(self, msg:str):
        ''' Emit a debug log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).debug, LOG_TEXT_COLORS.BLUE)

    def warn(self, msg:str):
        ''' Emit a warning log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).warn, LOG_TEXT_COLORS.YELLOW)

    def error(self, msg:str):
        ''' Emit an error log '''

        self._log(msg, logging.getLogger(self.LOGGER_NAME).error, LOG_TEXT_COLORS.RED)

    def critical(self, msg:str):
        ''' Emit a critical error log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).critical, LOG_TEXT_COLORS.PURPLE)
