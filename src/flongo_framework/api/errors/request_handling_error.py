from typing import Optional, Union

from ...api.responses.errors.api_error import API_Error

class RequestHandlingError(API_Error):
    ''' An error thrown while handling an API call.
        it contains a message, status code and optional
        stacktrace
    '''
    def __init__(self,
                 message:str = 'Error Handling Request',
                 data:Optional[dict] = None, 
                 status_code:int = 500, 
                 stack_trace:Union[str, None] = None
        ):

        self.message = message
        self.data = data or {}
        self.status_code = status_code
        self.stack_trace = stack_trace
