import logging
from src.config.enums.http_methods import HTTP_METHODS
from src.config.enums.log_levels import LOG_LEVELS
from src.config.settings.core.app_settings import AppSettings
from src.api.errors.schema_validation_error import SchemaValidationError

from src.api.responses.errors.api_error import API_Error
from src.database.mongodb.database import MongoDB_Database
from src.utils.logging.loggers.routing import RoutingLogger
from src.utils.requests import RequestDataParser, JSON_Schema_Validator
from src.api.errors.request_handling_error import RequestHandlingError

import traceback
from flask import Flask, Request, Response, jsonify, request
from werkzeug.exceptions import HTTPException
from typing import Callable, Optional
from .types import HandlerMethod


class RouteHandler:
    ''' Base class that allows functions to be bound
        to specific HTTP methods like GET or POST

        Used in conjuction with a Route to create an 
        object that contains a URL and supported methods
        that can be executed. This route can be "bound"
        to a Flask server
    '''

    # Holds a reference of all methods for this route
    def __init__(self, **methods:HandlerMethod):
        self.methods = {}
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
    

    def get_methods(self) -> dict[str, HandlerMethod]:
        ''' Returns all methods handled by this handler
            and their associated function
        '''

        return self.methods
    

    def _get_request_handler(self, url:str, method:str, action:HandlerMethod, collection_name:str, settings:AppSettings, request_schema:dict) -> Callable:
        ''' Delegates a request recieved by Flask to one
            of the methods registered to an instance of
            a Routehandler if possible
        '''

        def handler(**kwargs) -> Optional[Response]:
            RoutingLogger.info(f"* Recieved HTTP {method.upper()} request on URL [{url}] *")
            # Get the data from the request body or query params
            payload = RequestDataParser.get_request_data(request)
            RoutingLogger.debug(f"Parsed payload data for request: {payload}")
            try:
                # Validate the JSONSchema for this route if one is configured
                self._validate_schema(request, payload, request_schema)
                RoutingLogger.debug(f"Request schema for HTTP {method.upper()} on URL [{url}] validated!")
                # Execute the function configured for this route if one is configured
                # If there is a MongoDB collection specified, grab it and pass it too
                if collection_name:
                    with MongoDB_Database(collection_name, settings=settings.mongodb, connection_must_be_valid=True) as db:
                        RoutingLogger.debug(f"Passing connection to MongoDB collection [{collection_name}] with request")
                        response = action(request, payload, db)
                else:
                    response = action(request, payload, None)

                if not isinstance(response, Response):
                    RoutingLogger.warn(f"HTTP {method.upper()} response on URL [{url}] was force to a Response! Type: {type(response)}")
                    response = jsonify(response)
                        
                if response.json:
                    RoutingLogger.debug(f"Attaching response body [{response.json}]")
                
                RoutingLogger.info(f"* Sending HTTP {method.upper()} response on URL [{url}] *")
                return response
            except HTTPException as e:
                # Handle and log Flask generated errors
                self._log_and_raise_exception(
                    RequestHandlingError(f"[{method}] Error handling request on URL [{url}]!", status_code=e.code or 500),
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
                        f"Schema validation error on URL [{url}]: {e.message}",
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
        
        RoutingLogger.error(str(error))
        raise error
    

    def _validate_schema(self, request:Request, payload:dict, request_schema:dict):
        ''' Validate the request payload against a JSONSchema if one was supplied'''

        if request_schema:
            validator = JSON_Schema_Validator(request.url_root, request_schema)
            validator.validate_request(request.method.upper(), payload)
    

    def register_url_methods(self, url:str, collection_name:str, flask_app:Flask, settings:AppSettings, request_schema:dict):
        ''' Register the functions for all methods (like GET or POST)
            that are supported for a specified URL with Flask
        '''

        for method, action in self.get_methods().items():
            method_handler = self._get_request_handler(url, method, action, collection_name, settings, request_schema)
            flask_app.add_url_rule(url, f"{url}_{method}", method_handler, methods=[method.upper()])

            RoutingLogger.debug(f"Bound function for HTTP {method.upper()} on URL [{url}]")


    def configure_logger(self, log_level:str):
        logging.basicConfig(level=logging.NOTSET)

        # Routing
        logging.getLogger(RoutingLogger.LOGGER_NAME).setLevel(
            LOG_LEVELS.level_to_int(log_level)
        )