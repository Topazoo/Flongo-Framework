from src.responses import API_Error_Response
from src.logger import LoggingUtil
from src.routing.utils import RequestDataParser
from src.errors import Request_Handling_Error

import traceback
from flask import Flask, request
from flask.typing import RouteCallable
from werkzeug.exceptions import HTTPException
from typing import Callable

class RouteHandler:
    ''' Base class that allows functions to be bound
        to specific HTTP methods like GET or POST

        Used in conjuction with a Route to create an 
        object that contains a URL and supported methods
        that can be executed. This route can be "bound"
        to a Flask server
    '''

    # All methods a Routehandler can handle
    ALL_SUPPORTED_METHODS = [
        'get', 
        'post', 
        'put', 
        'patch', 
        'delete', 
        'options'
    ]

    # Holds a reference of all methods for this route
    methods:dict[str, Callable] = {}
    def __init__(self, **methods:Callable):
        for method, func in methods.items():
            normalized_method = method.lower()
            # Ensure the method is a valid HTTP method
            if normalized_method not in self.ALL_SUPPORTED_METHODS:
                raise ValueError(f"Routehandler: [{normalized_method}] is not a valid HTTP method.")

            # Create a function on this handler tied
            # for a method like GET tied to a function
            # that should run when it is called 
            setattr(self, normalized_method, func)
            self.methods[normalized_method] = func
    

    def get_methods(self) -> dict[str, Callable]:
        ''' Returns all methods handled by this handler
            and their associated function
        '''

        return self.methods
    

    def _get_request_handler(self, method:str, action:Callable) -> RouteCallable:
        ''' Delegates a request recieved by Flask to one
            of the methods registered to an instance of
            a Routehandler if possible
        '''

        def handler(**kwargs):
            try:
                # Get the data from the request body or query params
                payload = RequestDataParser.get_request_data(request)
                return action(request, payload)
            except API_Error_Response as e:
                # Handle user generated errors
                raise API_Error_Response(f"[{method.upper()}] ERROR: {e.message}", e.code)
            except HTTPException as e:
                # Handle and log Flask generated errors
                stack_trace = traceback.format_exc() # TODO - Only for debug
                error = Request_Handling_Error(method, str(e.description), e.code or 500, stack_trace)
                LoggingUtil.error(str(error))
                raise error
            except Exception as e:
                # Handle and log otherwise unhandled errors
                stack_trace = traceback.format_exc() # TODO - Only for debug
                error = Request_Handling_Error(method, str(e), 500, stack_trace)
                LoggingUtil.error(str(error))
                raise error
        return handler
    
    def register_url_methods(self, url:str, flask_app:Flask):
        ''' Register the functions for all methods (like GET or POST)
            that are supported for a specified URL with Flask
        '''

        for method, action in self.get_methods().items():
            method_handler = self._get_request_handler(method, action)
            method_handler.__name__ = f"{url}_{method}"  # To avoid Flask's AssertionError: View function mapping is overwriting an existing endpoint function
            flask_app.add_url_rule(url, method_handler.__name__, method_handler, methods=[method.upper()])
