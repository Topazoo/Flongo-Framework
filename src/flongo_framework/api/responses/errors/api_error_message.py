from ....api.responses.errors.api_error import API_Error

from typing import Optional

class API_Error_Message(API_Error):
    ''' An exception that can be thrown from
        user defined request handling functions
        to display a string error message response
    '''

    def __init__(self, message:str, data:Optional[dict] = None, status_code:int=500, stack_trace:Optional[str]=None):
        super(Exception, self).__init__(message)
        self._initialize(message, data, status_code, stack_trace)
