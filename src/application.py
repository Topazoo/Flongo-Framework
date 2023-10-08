from flask import Flask, jsonify
from src.config.configs.app_config import FlaskConfig
from src.errors.request_handling_error import Request_Handling_Error
from src.responses.api_error_response import API_Error_Response
from src.routing.route import Route
    
class Application:
    ''' Base application class that serves as a configuration class around Flask
        It allows us to extend the Flask application and add custom setup steps
        for our application like connecting to a database
    '''
    
    routes:dict[str, Route] = {}
    def __init__(self, config):
        # TODO - Config Class
        self.config = config

        self.app = Flask(__name__)
        self._initialize()


    def _initialize(self):
        # Set up all passed settings
        self.settings = self.config.get('settings', {})
        self._register_settings()

        # Create error handling definitions
        self._register_error_handlers()

        # Set up all passed Route definitions
        self.routes = self.config.get('routes', {})
        self._register_routes()


    def _register_settings(self):
        '''
            Register all settings specified in the Routes config
            to the application
        '''

        # TODO - Move to standalone driver(s)
        settings = self.settings

        # JWT settings
        jwt_settings = settings.get('jwt_settings', {})
        if jwt_settings.get('app_use_jwt'):
            # TODO - Implement JWT setup here
            pass

        # CORS
        if settings.get('app_settings', {}).get('app_enable_cors'):
            # TODO - integrate with Flask-CORS here
            pass


    def _register_routes(self):
        ''' Register all routes specified in the Routes config
            to the application
        '''

        for route in self.routes.values():
            route.register(self.app)


    def _register_error_handlers(self):
        ''' Register wrappers to handle specific kinds of errors '''

        @self.app.errorhandler(API_Error_Response)
        def handle_user_thrown_error(error:API_Error_Response):
            response = jsonify(message=error.message)
            response.status_code = error.code
            return response
        
        @self.app.errorhandler(Request_Handling_Error)
        def handle_request_exception(error:Request_Handling_Error):
            response = jsonify(message=str(error))
            response.status_code = error.status_code
            return response


    # TODO - Allow connection settings
    def run(self, host='127.0.0.1', port=3000):
        self.app.run(host=host, port=port)