from typing import Union

class RoutePermissions:
    ''' Base class that allows Permissions to be bound
        to specific HTTP methods like GET or POST

        Used in conjuction with a Route to hold Permissions
        for each method for request JWT validation
    '''

    GET = []
    POST = []
    PUT = []
    PATCH = []
    DELETE = []

    def __init__(self, 
            GET:Union[str, list[str]]='',
            POST:Union[str, list[str]]='',
            PUT:Union[str, list[str]]='',
            PATCH:Union[str, list[str]]='',
            DELETE:Union[str, list[str]]='',
        ) -> None:
            
            self.GET = self._normalize_value(GET)
            self.POST = self._normalize_value(POST)
            self.PUT = self._normalize_value(PUT)
            self.PATCH = self._normalize_value(PATCH)
            self.DELETE = self._normalize_value(DELETE)
        

    def _normalize_value(self, val:Union[str, list[str]]) -> list[str]:
        if not val:
            return []
        
        return [val] if not isinstance(val, list) else val
