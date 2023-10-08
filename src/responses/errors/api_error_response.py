# Encoding
from json import dumps
from typing import Any

class API_Error_Response(Exception):
    ''' An exception that can be thrown from
        user defined request handling functions
        that contains JSON data
    '''

    def __init__(self, data:Any, code:int=500):
        if not isinstance(data, dict):
            data = {'data': data}

        self.data = data
        self.code = code

    def to_response(self) -> str:
        return dumps({
            **self.data,
            'code': self.code
        })
