from flask_cors import cross_origin

from ....api.requests.request import App_Request
from ....api.routing.route_permissions import Route_Permissions
from ....api.routing.route_schema import Route_Schema
from ....config.enums.http_methods import HTTP_METHODS
from ....config.settings.app_settings import App_Settings
from ....api.errors.schema_validation_error import SchemaValidationError

from ....api.responses.errors.api_error import API_Error
from ....database.mongodb.database import MongoDB_Database
from ....utils.jwt.authentication_util import Authentication_Util
from ....utils.logging.loggers.routing import RoutingLogger
from ....utils.requests import RequestDataParser
from ....api.errors.request_handling_error import RequestHandlingError

import traceback
from flask import Flask, Response, jsonify, request
from werkzeug.exceptions import HTTPException
from typing import Callable, Optional
from sentry_sdk import start_span


class Route_Handler:
    ''' Base class that allows functions to be bound
        to specific HTTP methods like GET or POST

        Used in conjuction with a Route to create an 
        object that contains a URL and supported methods
        that can be executed. This route can be "bound"
        to a Flask server
    '''

    # Holds a reference of all methods for this route
    def __init__(self, **methods:Callable[[App_Request], Response]):
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
    

    def get_methods(self) -> dict[str, Callable[[App_Request], Response]]:
        ''' Returns all methods handled by this handler
            and their associated function
        '''

        return self.methods
    

    def _get_request_handler(
            self, 
            url:str,
            method:str, 
            action:Callable[[App_Request], Response], 
            collection_name:str,
            permissions:Route_Permissions,
            settings:App_Settings, 
            request_schema:Route_Schema,
            response_schema:Route_Schema
        ) -> Callable:
        ''' Delegates a request recieved by Flask to one
            of the methods registered to an instance of
            a Routehandler if possible
        '''
        
        logger = RoutingLogger(url, method)
        def handler(**kwargs) -> Optional[Response]:
            logger.info(f"* Recieved HTTP {method} request *")
            wrapped_request = App_Request(request)

            # Get the data from the request body or query params
            with start_span(op="parse_request_data", description="Parse data from the query string or request body"):
                wrapped_request.set_payload(RequestDataParser.get_request_data(wrapped_request.raw_request, logger))
            try:
                # Validate JIT roles
                if required_roles:=getattr(permissions, method, []):
                    with start_span(op="validate_jwt", description="Validate the passed JWT token"):
                        wrapped_request.set_identity(Authentication_Util.validate_identity_cookie_role(required_roles))
                        logger.info("* Validated request JWT IDENTITY successfully *")

                # Validate the payload passed to this route agains the request JSONSchema if configured
                with start_span(op="validate_request_schema", description="Validate the passed request data against the configured JSONSchema"):
                    if request_schema.validate_schema(wrapped_request.raw_request, wrapped_request.payload):
                        logger.info("* Validated request SCHEMA successfully")

                # Execute the function configured for this route if one is configured
                # If there is a MongoDB collection specified, grab it and pass it too
                if collection_name:
                    with start_span(op="open_database", description="Open a configured MongoDB collection"):
                        with MongoDB_Database(collection_name, settings=settings.mongodb, connection_must_be_valid=True) as db:
                            logger.debug(f"* Opened DATABASE CONNECTION to MongoDB collection [{collection_name}] for request")
                            wrapped_request.set_collection(db)

                with start_span(op="handle_request", description="Run user configured request handling logic"):
                    response = action(wrapped_request)

                with start_span(op="create_response", description="Create the final Flask response"):
                    if not isinstance(response, Response):
                        with start_span(op="convert_response", description="Convert a non-Response object to a Flask response"):
                            logger.warn(f"* HTTP {method} response was forced to a Response! Type: {type(response)}")
                            response = jsonify(response)

                    # Validate the payload passed to this route agains the request JSONSchema if configured    
                    with start_span(op="validate_response_schema", description="Validate the passed response data against the configured JSONSchema"):
                        if isinstance(response.json, dict) and response_schema.validate_schema(wrapped_request.raw_request, response.json, is_response_schema=True):
                            logger.info("* Validated response SCHEMA successfully")
                            
                    with start_span(op="deliver_response", description="Send the response"):
                        if response.json:
                            logger.debug(f"* Attached RESPONSE BODY [{response.json}]")
                        
                        logger.info(f"* Sending HTTP {method} response: ({response.status_code}) *")
                        return response
                    
            except HTTPException as e:
                # Handle and log Flask generated errors
                self._log_and_raise_exception(wrapped_request, method,
                    RequestHandlingError(f"[{method}] Error handling request on URL [{url}]!", status_code=e.code or 500),
                    settings,
                    logger
                )
            except API_Error as e:
                # Handle user generated errors
                self._log_and_raise_exception(wrapped_request, method, e, settings, logger)
            except SchemaValidationError as e:
                # Handle schema validation errors
                self._log_and_raise_exception(wrapped_request, method,
                    RequestHandlingError(
                        f"{'Response' if e.is_response_schema else 'Request'} schema validation error on URL [{url}]: {e.message}",
                        data=e.get_data(settings.flask.debug_mode),
                        status_code=400
                    ), 
                    settings,
                    logger
                )
            except Exception as e:
                # Handle unknown exceptions
                self._log_and_raise_exception(wrapped_request, method,
                    RequestHandlingError(str(e), status_code=500), settings, logger
                )
            
        return handler
    

    def _log_and_raise_exception(self, wrapped_request:App_Request, method:str, error:API_Error, settings:App_Settings, logger:RoutingLogger):
        ''' Log and raise an exception '''

        tb = traceback.format_exc()
        if settings.flask.debug_mode:
            error.update_payload_data("request_headers", list(wrapped_request.raw_request.headers))
            error.update_payload_data("request_data", wrapped_request.payload)
            error.set_stack_trace(tb)
        
        logger.error(f"* Error: {error}")
        logger.debug(tb)
        logger.info(f"* Sending HTTP {method} ERROR response: ({error.status_code}) *")

        raise error
    

    def register_url_methods(self, 
            url:str, 
            collection_name:str,
            permissions:Route_Permissions,
            enable_CORS:bool,
            flask_app:Flask,
            settings:App_Settings, 
            request_schema:Route_Schema,
            response_schema:Route_Schema, 
            log_level:str
        ):
        ''' Register the functions for all methods (like GET or POST)
            that are supported for a specified URL with Flask
        '''

        for method, action in self.get_methods().items():
            self.configure_logger(url, method, log_level)

            method_handler = self._get_request_handler(
                url, 
                method,
                action,
                collection_name,
                permissions,
                settings,
                request_schema,
                response_schema
            )

            # Enable CORS for the route if it is specified
            if enable_CORS: 
                method_handler = cross_origin(
                    origins=settings.flask.cors_origins,
                    supports_credentials=True
                )(method_handler)

            flask_app.add_url_rule(url, f"{url}_{method}", method_handler, methods=[method])
            RoutingLogger(url, method).debug(f"Function [{action.__name__}] bound to HTTP method")

        logger = RoutingLogger(url)
        logger.info(f"* CORS enabled for route: [{url}] *") if enable_CORS else RoutingLogger(url).info(f"* CORS disabled for route: {url} *")
        if method_permissions:=permissions.permissions_map:
            logger.info(f"* JWT validation enabled on methods: {list(method_permissions.keys())} *")
            logger.debug(f"JWT permissions: {method_permissions}")
        else:
            logger.info(f"* JWT validation disabled for route: {url} *")
    

    def configure_logger(self, url:str, method:str, log_level:str):
        RoutingLogger(url, method).create_logger(log_level)
