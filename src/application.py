import logging
from src.config.enums.log_levels import LOG_LEVELS
from src.config.settings import AppRoutes, AppSettings
from src.api.responses.errors.api_error import API_Error
from src.utils.json import JSON_Provider

from flask import Flask, jsonify
from typing import Optional

from src.utils.logging.loggers.app import ApplicationLogger
    
class Application:
    ''' Base application class that serves as a configuration class around Flask
        It allows us to extend the Flask application and add custom setup steps
        for our application like connecting to a database
    '''
    
    def __init__(self, routes:AppRoutes, settings:Optional[AppSettings]=None):
        # Get registered routes and settings
        self.app = Flask(__name__)
        self.routes = routes

        # Register as part of the Flask app config
        self.settings = settings or AppSettings()
        self.app.config['APP_SETTINGS'] = self.settings

        # Configure loggers
        self._configure_logger()

        # Initialize the application
        self._initialize()

        ApplicationLogger.info(f"App started successfully!")


    def _configure_logger(self):
        # Application
        logging.getLogger(ApplicationLogger.LOGGER_NAME).setLevel(
            LOG_LEVELS.level_to_int(self.settings.flask.log_level or '')
        )


    def _initialize(self):
        # Create error handling definitions
        self._register_error_handlers()

        # Register all passed Route definitions
        self.routes.register_routes(self.app, self.settings)

        # Set JSON encoding class
        self.app.json = JSON_Provider(self.app)


    def _register_error_handlers(self):
        ''' Register wrappers to handle specific kinds of errors '''
        
        @self.app.errorhandler(API_Error)
        def handle_user_thrown_error(error:API_Error):
            response = jsonify(
                error=error.message, 
                traceback=error.stack_trace, 
                additional_data=error.data,
            )
            response.status_code = error.status_code
            return response


    def run(self):
        self.app.run(
            host=self.settings.flask.host,
            port=self.settings.flask.port,
            debug=self.settings.flask.debug_mode,
        )