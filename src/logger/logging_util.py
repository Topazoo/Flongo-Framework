import logging
from typing import Callable

class LoggingUtil:
    ''' Base logger class for the application '''

    @classmethod
    def info(cls, msg:str):
        ''' Emit a info log '''
        cls._log(msg, logging.info)


    @classmethod
    def debug(cls, msg:str):
        ''' Emit a debug log '''
        cls._log(msg, logging.debug)


    @classmethod
    def warn(cls, msg:str):
        ''' Emit a warning log '''
        cls._log(msg, logging.warn)


    @classmethod
    def error(cls, msg:str):
        ''' Emit an error log '''
        cls._log(msg, logging.error)


    @classmethod
    def critical(cls, msg:str):
        ''' Emit a critical error log '''
        cls._log(msg, logging.critical)


    @classmethod
    def _log(cls, msg:str, logging_func:Callable=print):
        ''' Emit a log. Optionally emit using a passed function '''

        logging_func(msg)
