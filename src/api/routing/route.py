import logging
from typing import Optional
from flask import Flask
from src.api.routing.route_permissions import Route_Permissions
from src.config.enums.logs.log_levels import LOG_LEVELS
from src.config.settings.app_settings import App_Settings
from src.utils.logging.loggers.routing import RoutingLogger
from src.api.routing.handlers.route_handler import Route_Handler
from src.api.routing.route_schema import Route_Schema

class Route:
    ''' Base class that wraps Flasks normal routing allowing us
        to pick up configured parameters like the database to 
        connect to or the permissions required to access the 
        endpoint
    '''

    def __init__(self, 
            url:str, 
            handler:Route_Handler,
            permissions:Optional[Route_Permissions]=None,
            enable_CORS:bool=True,
            collection_name:str='',
            request_schema:Optional[Route_Schema]=None,
            response_schema:Optional[Route_Schema]=None,
            log_level:str=LOG_LEVELS.WARN
        ):

        self.url = url
        self.handler = handler
        self.permissions = permissions or Route_Permissions()
        self.enable_CORS = enable_CORS
        self.collection_name = collection_name
        self.request_schema = request_schema or Route_Schema()
        self.response_schema = response_schema or Route_Schema()
        self.log_level = log_level

        self._configure_logger()
    
    
    def register(self, flask_app:Flask, settings:App_Settings):
        ''' Registers this URL to a Flask app and binds all supplied
            methods (e.g. GET or POST) specified in the passed RouteHandler
        '''

        self.handler.register_url_methods(
            self.url,
            self.collection_name,
            self.permissions,
            self.enable_CORS,
            flask_app, 
            settings, 
            self.request_schema,
            self.response_schema,
            self.log_level
        )

        RoutingLogger(self.url).info(f"* Created application route: [{self.url}] *")


    def _configure_logger(self):
        RoutingLogger(self.url).create_logger(self.log_level)
