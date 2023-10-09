from typing import Union
from flask.json.provider import JSONProvider
from .json_encoder import JSON_Encoder
import json

class JSON_Provider(JSONProvider):
    
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=JSON_Encoder)
    
    def loads(self, s: Union[str, bytes], **kwargs):
        return json.loads(s, **kwargs)
