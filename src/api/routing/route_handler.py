from src.config.enums.http_methods import HTTP_METHODS
from src.config.settings.core.app_settings import AppSettings
from src.api.errors.schema_validation_error import SchemaValidationError

from src.api.responses.errors.api_error import API_Error
from src.utils.requests import RequestDataParser, JSON_Schema_Validator
from src.api.errors.request_handling_error import RequestHandlingError

import traceback
from flask import Flask, Request, Response, request
from werkzeug.exceptions import HTTPException
from typing import Callable, Optional
from src.utils.logging.logging_util import LoggingUtil


class RouteHandler:
    ''' Base class that allows functions to be bound
        to specific HTTP methods like GET or POST

        Used in conjuction with a Route to create an 
        object that contains a URL and supported methods
        that can be executed. This route can be "bound"
        to a Flask server
    '''

    # Holds a reference of all methods for this route
    methods:dict[str, Callable] = {}
    def __init__(self, **methods:Callable):
        for method, func in methods.items():
            normalized_method = method.lower()
            # Ensure the method is a valid HTTP method
            if normalized_method not in HTTP_METHODS.ALL:
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
    

    def _get_request_handler(self, method:str, action:Callable, settings:AppSettings, request_schema:dict) -> Callable:
        ''' Delegates a request recieved by Flask to one
            of the methods registered to an instance of
            a Routehandler if possible
        '''

        def handler(**kwargs) -> Optional[Response]:
            # Get the data from the request body or query params
            payload = RequestDataParser.get_request_data(request)
            try:
                # Validate the JSONSchema for this route if one is configured
                self._validate_schema(request, payload, request_schema, settings)
                # Execute the function configured for this route if one is configured
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
            except SchemaValidationError as e:
                # Handle schema validation errors
                self._log_and_raise_exception(
                    RequestHandlingError(
                        f"Schema validation error: {e.message}",
                        data=e.get_data(settings.flask.debug_mode),
                        status_code=400
                    ), 
                    payload, 
                    settings
                )
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
    

    def _validate_schema(self, request:Request, payload:dict, request_schema:dict, settings:AppSettings):
        ''' Validate the request payload against a JSONSchema if one was supplied'''

        if request_schema:
            validator = JSON_Schema_Validator(request.url_root, request_schema)
            validator.validate_request(request.method.upper(), payload)
    

    def register_url_methods(self, url:str, flask_app:Flask, settings:AppSettings, request_schema:dict):
        ''' Register the functions for all methods (like GET or POST)
            that are supported for a specified URL with Flask
        '''

        for method, action in self.get_methods().items():
            method_handler = self._get_request_handler(method, action, settings, request_schema)
            method_handler.__name__ = f"{url}_{method}"  # To avoid Flask's AssertionError: View function mapping is overwriting an existing endpoint function
            flask_app.add_url_rule(url, method_handler.__name__, method_handler, methods=[method.upper()])