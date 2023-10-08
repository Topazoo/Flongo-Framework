from src.config import AppRoutes, AppSettings
from src.responses import API_Error_Response, API_Error_Message
from src.errors import RequestHandlingError

from typing import Optional, Union
from flask import Flask, jsonify

from src.responses.errors.api_error import API_Error
from src.routing.utils.json_provider import JSON_Provider
    
class Application:
    ''' Base application class that serves as a configuration class around Flask
        It allows us to extend the Flask application and add custom setup steps
        for our application like connecting to a database
    '''
    
    def __init__(self, routes:AppRoutes, settings:Optional[AppSettings]=None):
        # Get registered routes and settings
        self.app = Flask(__name__)

        self.routes = routes
        self.settings = settings or AppSettings()

        # Register as part of the Flask app config
        self.app.config['APP_SETTINGS'] = self.settings

        self._initialize()


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