from src.config.settings.core.app_settings import AppSettings
from src.responses import API_Error_Response
from src.logger import LoggingUtil
from src.responses.errors.api_error import API_Error
from src.responses.errors.api_error_message import API_Error_Message
from src.routing.utils import RequestDataParser
from src.errors import RequestHandlingError

import traceback
from flask import Flask, Response, request
from flask.typing import RouteCallable
from werkzeug.exceptions import HTTPException
from typing import Callable, Optional

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
    

    def _get_request_handler(self, method:str, action:Callable, settings:AppSettings) -> Callable:
        ''' Delegates a request recieved by Flask to one
            of the methods registered to an instance of
            a Routehandler if possible
        '''

        def handler(**kwargs) -> Optional[Response]:
            # Get the data from the request body or query params
            payload = RequestDataParser.get_request_data(request)
            try:
                return action(request, payload)
            except HTTPException as e:
                # Handle and log Flask generated errors
                self._log_and_raise_exception(
                    RequestHandlingError(f"[{method}] Error handling request!", status_code=e.code or 500),
                    payload,
                    settings
                )
            except API_Error as e:
                # Handle user generated errors
                self._log_and_raise_exception(e, payload, settings)
            except Exception as e:
                # Handle unknown exceptions
                self._log_and_raise_exception(
                    RequestHandlingError(str(e), status_code=500), payload, settings
                )
            
        return handler
    
    def _log_and_raise_exception(self, error:API_Error, payload:dict, settings:AppSettings):
        ''' Log and raise an exception '''

        if settings.flask.debug_mode:
            error.update_payload_data("request_headers", list(request.headers))
            error.update_payload_data("request_data", payload)
            error.set_stack_trace(traceback.format_exc())
        
        LoggingUtil.error(str(error))
        raise error
    
    def register_url_methods(self, url:str, flask_app:Flask, settings:AppSettings):
        ''' Register the functions for all methods (like GET or POST)
            that are supported for a specified URL with Flask
        '''

        for method, action in self.get_methods().items():
            method_handler = self._get_request_handler(method, action, settings)
            method_handler.__name__ = f"{url}_{method}"  # To avoid Flask's AssertionError: View function mapping is overwriting an existing endpoint function
            flask_app.add_url_rule(url, method_handler.__name__, method_handler, methods=[method.upper()])
