import logging
from typing import Callable

import logging

from src.config.enums.log_levels import LOG_LEVELS

class LoggingUtil:
    ''' Base logger class for the application '''

    LOGGER_NAME = "root"

    @classmethod
    def info(cls, msg:str):
        ''' Emit a info log '''
        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).info)


    @classmethod
    def debug(cls, msg:str):
        ''' Emit a debug log '''
        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).debug)


    @classmethod
    def warn(cls, msg:str):
        ''' Emit a warning log '''
        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).warn)


    @classmethod
    def error(cls, msg:str):
        ''' Emit an error log '''

        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).error)


    @classmethod
    def critical(cls, msg:str):
        ''' Emit a critical error log '''

        cls._log(msg, logging.getLogger(cls.LOGGER_NAME).critical)


    @classmethod
    def _log(cls, msg:str, logging_func:Callable=print):
        ''' Emit a log. Optionally emit using a passed function '''

        logging_func(msg)


    @staticmethod
    def log_level_int(log_level:str) -> int:
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
