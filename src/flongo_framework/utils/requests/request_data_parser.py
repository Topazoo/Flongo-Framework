

from typing import Optional
import xmltodict
from flask import Request
from QueryStringManager import QueryStringManager
from ...utils.logging.loggers.routing import RoutingLogger


class RequestDataParser:
    ''' Utility class that supports parsing a request query parameters
        or body into a dictionary to be consumed by the function
        specified in the handler for the HTTP method of the request    
    '''

    @classmethod
    def get_request_data(cls, request:Request, logger:Optional[RoutingLogger]=None) -> dict:
        ''' Gets the request data from a Flask request body
            or query string
        '''

        query_string_params = cls.parse_query_string(request, logger)
        request_body_params = cls.parse_request_body(request, logger)

        return {**query_string_params, **request_body_params}


    @classmethod
    def parse_query_string(cls, request:Request, logger:Optional[RoutingLogger]=None) -> dict:
        ''' Parse a query string into a dictionary if one is present '''

        query_string_params = QueryStringManager.parse(request.query_string.decode()) if \
            request.query_string else {}
        
        if query_string_params and logger:
            logger.debug(f"* Parsed QUERY STRING data for request: {query_string_params}")

        return query_string_params


    @classmethod
    def parse_request_body(cls, request:Request, logger:Optional[RoutingLogger]=None) -> dict:
        ''' Parse the request body into a dictionary if one is present '''

        body = {}
        mimetype_suffix = request.mimetype.split('/')[-1]
        if request.is_json:
            body = request.get_json()
        
        elif mimetype_suffix == 'plain' and request.data:
            body = {"data": request.data.decode()}
        
        # TODO - Extend to just form present?
        elif mimetype_suffix in ['x-www-form-urlencoded', 'form-data']:
            body = request.form.to_dict()
        
        elif mimetype_suffix in ['xml', 'html']:
            body = xmltodict.parse(request.data.decode())
        
        elif request.mimetype and logger:
            logger.error(f"* Unable to parse mimetype [{request.mimetype}]!")
        
        if body and logger:
            logger.debug(f"* Parsed REQUEST BODY with MIME type [{request.mimetype}]: {body}")
        
        return body
