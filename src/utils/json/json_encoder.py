
from datetime import datetime
from json import JSONEncoder
from decimal import Decimal

from src.utils.logging.logging_util import LoggingUtil

class JSON_Encoder(JSONEncoder):
    ''' Custom JSON serializer '''

    def default(self, obj):
        try:
            # Handle dates
            if isinstance(obj, datetime):
                return obj.strftime("%c")
            
            # Handle sets
            if isinstance(obj, set):
                return tuple(obj)
            
            # Handle decimals
            if isinstance(obj, Decimal):
                return str(obj)
                
            return JSONEncoder.default(self, obj)
        except TypeError:   # Write as string on failure
            LoggingUtil.warn(f"JSON_Encoder: Could not serialize type [{type(obj)}]")
            
            return str(obj)