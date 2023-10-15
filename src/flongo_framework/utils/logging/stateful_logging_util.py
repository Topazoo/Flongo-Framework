import logging
from ...config.enums.logs.log_groups import LOG_GROUPS
from ...utils.logging.logging_util import LoggingUtil

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
        self._log(msg, logging.getLogger(self.LOGGER_NAME).info)

    def debug(self, msg:str):
        ''' Emit a debug log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).debug)

    def warn(self, msg:str):
        ''' Emit a warning log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).warn)

    def error(self, msg:str):
        ''' Emit an error log '''

        self._log(msg, logging.getLogger(self.LOGGER_NAME).error)

    def critical(self, msg:str):
        ''' Emit a critical error log '''
        self._log(msg, logging.getLogger(self.LOGGER_NAME).critical)


    def create_logger(self, log_level:str, format:str=''):
        ''' Create a logger with a built-in color formatter '''

        return self._create_logger(self.LOGGER_NAME, log_level, format)