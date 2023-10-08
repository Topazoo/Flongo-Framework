from typing import Any, Optional

class API_Error(Exception):
    ''' An base exception that can be thrown from
        user defined request handling functions
        to display a string error message response
    '''

    def __init__(self, message:Any, data:Optional[dict] = None, status_code:int=500, stack_trace:Optional[str]=None):
        super(Exception, self).__init__(message)
        self._initialize(message, data, status_code, stack_trace)


    def _initialize(self, message:Any, data:Optional[dict] = None, status_code:int=500, stack_trace:Optional[str]=None):
        self.message = message
        self.status_code = status_code
        self.stack_trace = stack_trace

        self.data = data or {}


    def set_stack_trace(self, stack_trace:str):
        self.stack_trace = stack_trace


    def update_payload_data(self, key:str, value:Any):
        self.data[key] = value
