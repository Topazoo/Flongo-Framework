
from datetime import datetime
from json import JSONEncoder
from decimal import Decimal

from bson import ObjectId

from ...utils.logging.loggers.app import ApplicationLogger

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
            
            # Handle ObjectIds
            if isinstance(obj, ObjectId):
                return str(obj)
                
            return JSONEncoder.default(self, obj)
        except TypeError:   # Write as string on failure
            ApplicationLogger.warn(f"JSON_Encoder: Could not serialize type [{type(obj)}]")
            
            return str(obj)