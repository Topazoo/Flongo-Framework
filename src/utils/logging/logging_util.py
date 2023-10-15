import logging
from typing import Callable

from src.config.enums.logs.log_levels import LOG_LEVELS
from src.utils.logging.formatters.colored_formatter import ColoredFormatter

class LoggingUtil:
    ''' Base logger class for the application '''

    LOGGER_NAME = "root"
    EMPTY_TRACEBACK = "NoneType: None\n"
    DEFAULT_FORMAT = "%(levelname)s:%(name)s:%(message)s"

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
        ''' Emit a log. Optionally emit using a passed function and color '''

        logging_func(msg)


    @classmethod
    def create_logger(cls, log_level:str, format:str=''):
        ''' Create a logger with a built-in color formatter '''

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LOG_LEVELS.level_to_int(LOG_LEVELS.DEBUG))
        formatter = ColoredFormatter(format or cls.DEFAULT_FORMAT)
        stream_handler.setFormatter(formatter)
        logger = logging.getLogger(cls.LOGGER_NAME)
        logger.setLevel(LOG_LEVELS.level_to_int(log_level))
        logger.addHandler(stream_handler)

        return logger