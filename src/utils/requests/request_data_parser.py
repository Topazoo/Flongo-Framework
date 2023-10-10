

import xmltodict
from flask import Request
from QueryStringManager import QueryStringManager
from src.utils.logging.loggers.routing import RoutingLogger


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

        query_string_params = QueryStringManager.parse(request.query_string.decode()) if \
            request.query_string else {}
        
        if query_string_params:
            RoutingLogger.debug(f"Parsed QUERY STRING data for request: {query_string_params}")

        return query_string_params


    @classmethod
    def parse_request_body(cls, request:Request) -> dict:
        ''' Parse the request body into a dictionary if one is present '''

        body = {}
        if request.is_json:
            body = request.get_json()
        
        mimetype_suffix = request.mimetype.split('/')[-1]
        if mimetype_suffix == 'plain' and request.data:
            body = {"data": request.data.decode()}
        
        # TODO - Extend to just form present?
        elif mimetype_suffix in ['x-www-form-urlencoded', 'form-data']:
            body = request.form.to_dict()
        
        elif mimetype_suffix in ['xml', 'html']:
            body = xmltodict.parse(request.data.decode())
        
        elif request.mimetype:
            RoutingLogger.error(f"Unable to parse mimetype [{request.mimetype}]!")
        
        if body:
            RoutingLogger.debug(f"Parsed REQUEST BODY data for MIME type [{request.mimetype}]: {body}")
        
        return body
