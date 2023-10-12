import logging
from src.config.enums.logs.colors.log_background_colors import LOG_BACKGROUND_COLORS
from src.config.enums.logs.log_levels import LOG_LEVELS
from src.config.settings import AppRoutes, AppSettings
from src.api.responses.errors.api_error import API_Error
from src.database.mongodb.database import MongoDB_Database
from src.database.mongodb.fixture.fixtures import MongoDB_Fixtures
from src.database.mongodb.index.indices import MongoDB_Indices
from src.utils.json import JSON_Provider

from flask import Flask, jsonify
from typing import Optional

from src.utils.logging.loggers.app import ApplicationLogger
    
class Application:
    ''' Base application class that serves as a configuration class around Flask
        It allows us to extend the Flask application and add custom setup steps
        for our application like connecting to a database
    '''
    
    def __init__(self, 
            routes:AppRoutes, 
            settings:Optional[AppSettings]=None,
            indices:Optional[MongoDB_Indices]=None,
            fixtures:Optional[MongoDB_Fixtures]=None
        ):
        # Get registered routes, settings, indices and fixtures
        self.app = Flask(__name__)
        self.routes = routes
        self.indices = indices
        self.fixtures = fixtures

        # Register as part of the Flask app config
        self.settings = settings or AppSettings()
        self.app.config['APP_SETTINGS'] = self.settings

        # Configure loggers
        self._configure_logger()

        # Initialize the application
        self._initialize()

        # Initialize the database and store client for re-use
        database = self._initialize_database()
        self.app.config['APP_DB_CLIENT'] = database.get_client()

        ApplicationLogger.critical(
            ApplicationLogger.color_log(f"[App Started Successfully]", LOG_BACKGROUND_COLORS.PURPLE)
        )


    def _configure_logger(self):
        # Application
        if self.settings.flask and self.settings.flask.log_level:
            logging.getLogger(ApplicationLogger.LOGGER_NAME).setLevel(
                LOG_LEVELS.level_to_int(self.settings.flask.log_level)
            )


    def _initialize(self):
        # Create error handling definitions
        self._register_error_handlers()

        # Register all passed Route definitions
        self.routes.register_routes(self.app, self.settings)

        # Set JSON encoding class
        self.app.json = JSON_Provider(self.app)

    
    def _initialize_database(self) -> MongoDB_Database:
        # Set up database driver
        database = MongoDB_Database(
            settings=self.settings.mongodb,
            indices=self.indices,
            fixtures=self.fixtures,
            connection_must_be_valid=True
        )

        # Create indices
        if self.indices and len(self.indices):
            database.create_indices()
            ApplicationLogger.critical(
                ApplicationLogger.color_log(
                    f"[Created [{len(self.indices)}] database {'indices' if len(self.indices) > 1 else 'index'}]",
                    LOG_BACKGROUND_COLORS.PURPLE
                )
            )

        # Create fixtures
        if self.fixtures and len(self.fixtures):
            database.create_fixtures()
            ApplicationLogger.critical(
                ApplicationLogger.color_log(
                    f"[Created [{len(self.fixtures)}] database fixture{'s' if len(self.fixtures) > 1 else ''}]",
                    LOG_BACKGROUND_COLORS.PURPLE
                )
            )

        return database

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