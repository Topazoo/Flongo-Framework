from json import dumps
from flask import Response
from typing import Any

from ...utils.json.json_encoder import JSON_Encoder

class API_JSON_Response(Response):
    ''' An JSON response that can be returned from
        user defined request handling functions

        If a primitive data type is passed, it will be set in 
        the response JSON with the key 'data'
    '''

    def __init__(self, data:Any, status_code:int=200) -> None:
        if not isinstance(data, dict):
            data = {'data': data}

        super().__init__(dumps(data, cls=JSON_Encoder), status=status_code, mimetype='application/json')
