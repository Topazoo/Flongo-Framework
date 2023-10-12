import logging
from src.config.enums.http_methods import HTTP_METHODS
from src.config.enums.logs.colors.log_background_colors import LOG_BACKGROUND_COLORS
from src.config.enums.logs.log_levels import LOG_LEVELS
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
            normalized_method = method.upper()
            # Ensure the method is a valid HTTP method
            if normalized_method.lower() not in HTTP_METHODS:
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
        
        logger = RoutingLogger(url, method)
        def handler(**kwargs) -> Optional[Response]:
            logger.info(logger.color_log(f"* Recieved HTTP {method} request *", LOG_BACKGROUND_COLORS.GREEN))
            # Get the data from the request body or query params
            payload = RequestDataParser.get_request_data(request, logger)
            try:
                # Validate the JSONSchema for this route if one is configured
                self._validate_schema(request, payload, request_schema, logger)
                # Execute the function configured for this route if one is configured
                # If there is a MongoDB collection specified, grab it and pass it too
                if collection_name:
                    with MongoDB_Database(collection_name, settings=settings.mongodb, connection_must_be_valid=True) as db:
                        logger.debug(f"* Opened DATABASE CONNECTION to MongoDB collection [{collection_name}] for request")
                        response = action(request, payload, db)
                else:
                    response = action(request, payload, None)

                if not isinstance(response, Response):
                    logger.warn(f"* HTTP {method} response was forced to a Response! Type: {type(response)}")
                    response = jsonify(response)
                        
                if response.json:
                    logger.debug(f"* Attached RESPONSE BODY [{response.json}]")
                
                logger.info(logger.color_log(f"* Sending HTTP {method} response *", LOG_BACKGROUND_COLORS.GREEN))
                return response
            except HTTPException as e:
                # Handle and log Flask generated errors
                self._log_and_raise_exception(url, method,
                    RequestHandlingError(f"[{method}] Error handling request on URL [{url}]!", status_code=e.code or 500),
                    payload,
                    settings,
                    logger
                )
            except API_Error as e:
                # Handle user generated errors
                self._log_and_raise_exception(url, method, e, payload, settings, logger)
            except SchemaValidationError as e:
                # Handle schema validation errors
                self._log_and_raise_exception(url, method,
                    RequestHandlingError(
                        f"Schema validation error on URL [{url}]: {e.message}",
                        data=e.get_data(settings.flask.debug_mode),
                        status_code=400
                    ), 
                    payload, 
                    settings,
                    logger
                )
            except Exception as e:
                # Handle unknown exceptions
                self._log_and_raise_exception(url, method,
                    RequestHandlingError(str(e), status_code=500), payload, settings, logger
                )
            
        return handler
    

    def _log_and_raise_exception(self, url:str, method:str, error:API_Error, payload:dict, settings:AppSettings, logger:RoutingLogger):
        ''' Log and raise an exception '''

        tb = traceback.format_exc()
        if settings.flask.debug_mode:
            error.update_payload_data("request_headers", list(request.headers))
            error.update_payload_data("request_data", payload)
            error.set_stack_trace(tb)
        
        logger.error(logger.color_log(f"* Error: {error}", LOG_BACKGROUND_COLORS.RED))
        logger.debug(tb)
        logger.info(logger.color_log(f"* Sending HTTP {method} ERROR response *", LOG_BACKGROUND_COLORS.GREEN))

        raise error
    

    def _validate_schema(self, request:Request, payload:dict, request_schema:dict, logger:RoutingLogger):
        ''' Validate the request payload against a JSONSchema if one was supplied'''

        if request_schema:
            validator = JSON_Schema_Validator(request.url_root, request_schema)
            validator.validate_request(request.method.upper(), payload)
            logger.info(f"* Validated SCHEMA successfully")
    

    def register_url_methods(self, url:str, collection_name:str, flask_app:Flask, settings:AppSettings, request_schema:dict, log_level:str):
        ''' Register the functions for all methods (like GET or POST)
            that are supported for a specified URL with Flask
        '''

        for method, action in self.get_methods().items():
            self.configure_logger(url, method, log_level)

            method_handler = self._get_request_handler(url, method, action, collection_name, settings, request_schema)
            flask_app.add_url_rule(url, f"{url}_{method}", method_handler, methods=[method])

            RoutingLogger(url, method).debug(f"Function [{action.__name__}] bound to HTTP method")


    def configure_logger(self, url:str, method:str, log_level:str):
        logging.basicConfig(level=logging.NOTSET)

        # Routing
        logging.getLogger(RoutingLogger(url, method).LOGGER_NAME).setLevel(
            LOG_LEVELS.level_to_int(log_level)
        )