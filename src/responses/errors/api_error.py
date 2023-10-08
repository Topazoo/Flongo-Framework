# Encoding
from typing import Any, Optional

class API_Error(Exception):
    ''' An base exception that can be thrown from
        user defined request handling functions
        to display a string error message response
    '''

    def __init__(self, message:str, data:Optional[dict] = None, status_code:int=500, stack_trace:Optional[str]=None):
        self.message = message
        self.status_code = status_code
        self.data = data or {}
        super(Exception, self).__init__(message)

    def set_stack_trace(self, stack_trace:str):
        self.stack_trace = stack_trace

    def update_payload_data(self, key:str, value:Any):
        self.data[key] = value
