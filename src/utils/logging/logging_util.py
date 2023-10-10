import logging
from typing import Callable, Optional

import logging

from src.config.enums import LOG_FOREGROUND_COLORS

class LoggingUtil:
    ''' Base logger class for the application '''

    LOGGER_NAME = "root"

    @classmethod
    def info(cls, msg:str):
        ''' Emit a info log '''
        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).info, LOG_FOREGROUND_COLORS.GREEN)


    @classmethod
    def debug(cls, msg:str):
        ''' Emit a debug log '''
        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).debug, LOG_FOREGROUND_COLORS.BLUE)


    @classmethod
    def warn(cls, msg:str):
        ''' Emit a warning log '''
        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).warn, LOG_FOREGROUND_COLORS.YELLOW)


    @classmethod
    def error(cls, msg:str):
        ''' Emit an error log '''

        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).error, LOG_FOREGROUND_COLORS.RED)


    @classmethod
    def critical(cls, msg:str):
        ''' Emit a critical error log '''

        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).critical, LOG_FOREGROUND_COLORS.PURPLE)


    @classmethod
    def _log(cls, msg:str, logging_func:Callable=print, color:Optional[str]=None):
        ''' Emit a log. Optionally emit using a passed function and color '''

        logging_func(msg if not color else cls.color_log(msg, color))


    @classmethod
    def color_log(cls, msg:str, color:str) -> str:
        return f"{color}{msg}{LOG_FOREGROUND_COLORS.END}"
