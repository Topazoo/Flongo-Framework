from ....api.responses.errors.api_error import API_Error

from typing import Any, Optional

class API_Error_Response(API_Error):
    ''' An exception that can be thrown from
        user defined request handling functions
        that contains JSON data
    '''

    def __init__(self, message:Any, data:Optional[dict] = None, status_code:int=500, stack_trace:Optional[str]=None):
        if not isinstance(message, dict):
            message = {'data': message}

        self._initialize(message, data, status_code, stack_trace)
