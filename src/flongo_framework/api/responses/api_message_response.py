from json import dumps
from flask import Response
from typing import Any

from ...utils.json.json_encoder import JSON_Encoder


class API_Message_Response(Response):
    ''' An string response that can be returned from
        user defined request handling functions
    '''

    def __init__(self, message:Any, status_code:int=200) -> None:
        super().__init__(dumps(message, cls=JSON_Encoder), status=status_code, mimetype='text/plain')
