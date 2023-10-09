

import xmltodict
from flask import Request
from QueryStringManager import QueryStringManager

from src.utils.logging.logging_util import LoggingUtil

class RequestDataParser:
    ''' Utility class that supports parsing a request query parameters
        or body into a dictionary to be consumed by the function
        specified in the handler for the HTTP method of the request    
    '''

    @classmethod
    def get_request_data(cls, request:Request) -> dict:
        ''' Gets the request data from a Flask request body
            or query string
        '''

        query_string_params = cls.parse_query_string(request)
        request_body_params = cls.parse_request_body(request)

        return {**query_string_params, **request_body_params}


    @classmethod
    def parse_query_string(cls, request:Request) -> dict:
        ''' Parse a query string into a dictionary if one is present '''

        return QueryStringManager.parse(request.query_string.decode()) if \
            request.query_string else {}


    @classmethod
    def parse_request_body(cls, request:Request) -> dict:
        ''' Parse the request body into a dictionary if one is present '''

        if request.is_json:
            return request.get_json()
        
        elif request.mimetype in [
            'application/x-www-form-urlencoded',
            'application/form-data',
            'multipart/form-data',
        ]:
            return request.form.to_dict()
        
        elif request.mimetype in [
            'text/xml',
            'application/xml',
            'text/html',
            'application/html',
        ]:
            return xmltodict.parse(request.data.decode())
        
        elif request.mimetype:
            LoggingUtil.error(f"RequestDataParser: Unable to parse mimetype [{request.mimetype}]!")
        
        return {}
