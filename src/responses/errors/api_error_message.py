from src.responses.errors.api_error import API_Error

from typing import Optional

class API_Error_Message(API_Error):
    ''' An exception that can be thrown from
        user defined request handling functions
        to display a string error message response
    '''

    def __init__(self, message:str, status_code:int=500, stack_trace:Optional[str]=None):
        super(Exception, self).__init__(message)
        self.message = message
        self.status_code = status_code
        self.stack_trace = stack_trace

        self.data = {}
