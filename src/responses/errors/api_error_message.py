# Encoding
from json import dumps

class API_Error_Message(Exception):
    ''' An exception that can be thrown from
        user defined request handling functions
        to display a string error message response
    '''

    def __init__(self, message:str, code:int):
        super(Exception, self).__init__(message)
        self.message = message
        self.code = code

    def to_response(self):
        return dumps({
            'error': self.message,
            'code': self.code
        })
