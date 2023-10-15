import logging
import traceback

from flask_cors import cross_origin
import sentry_sdk
from .api.routing import App_Routes
from .config.settings import App_Settings
from .api.responses.errors.api_error import API_Error
from .database.mongodb.database import MongoDB_Database
from .database.mongodb.fixture.fixtures import MongoDB_Fixtures
from .database.mongodb.index.indices import MongoDB_Indices
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from .utils.json import JSON_Provider

from flask import Flask, jsonify
from typing import Optional

from .utils.logging.loggers.app import ApplicationLogger
from .utils.jwt.jwt_manager import App_JWT_Manager
    
class Application:
    ''' Base application class that serves as a configuration class around Flask
        It allows us to extend the Flask application and add custom setup steps
        for our application like connecting to a database
    '''
    
    def __init__(self, 
            routes:App_Routes, 
            settings:Optional[App_Settings]=None,
            indices:Optional[MongoDB_Indices]=None,
            fixtures:Optional[MongoDB_Fixtures]=None
        ):
        # Get registered routes, settings, indices and fixtures
        self.settings = settings or App_Settings()
        self.routes = routes
        self.indices = indices
        self.fixtures = fixtures

        # Configure loggers
        self._configure_logger()

        # Initialize Sentry
        self._initialize_sentry()

        # Create the Flask app
        self.app = Flask(__name__)

        # Initialize JWT Util
        self._initialize_jwt()

        # Initialize the application
        self._initialize()

        # Initialize the database and store client for re-use
        if database:=self._initialize_database():
            self.app.config['APP_DB_CLIENT'] = database.get_client()

        if self.settings.flask.log_boot_events:
            ApplicationLogger.critical(f"[App Started Successfully]")


    def _configure_logger(self):
        # Application
        if self.settings.flask and self.settings.flask.log_level:
            ApplicationLogger.create_logger(self.settings.flask.log_level)


    def _initialize(self):
        # Store passed settings in the Flask app config
        self.app.config['APP_SETTINGS'] = self.settings

        # Create error handling definitions
        self._register_error_handlers()

        # Register all passed Route definitions
        self.routes.register_routes(self.app, self.settings)

        # Set JSON encoding class
        self.app.json = JSON_Provider(self.app)


    def _initialize_jwt(self):
        App_JWT_Manager(self.app, self.settings.jwt)


    def _initialize_sentry(self):
        if self.settings.sentry.dsn:
            try:
                sentry_sdk.init(
                    dsn=self.settings.sentry.dsn,
                    traces_sample_rate=float(self.settings.sentry.traces_sample_rate or "1.0"),
                    profiles_sample_rate=float(self.settings.sentry.profiles_sample_rate or "1.0"),
                    environment=self.settings.flask.env,
                    integrations=[
                        FlaskIntegration(),
                        LoggingIntegration(
                            level=logging.INFO,  # Capture info and above as breadcrumbs
                            event_level=logging.ERROR  # Send errors as events
                        )
                    ]
                )
                if self.settings.flask.log_boot_events:
                    ApplicationLogger.critical(f"[Connected to Sentry]")
            except Exception as e:
                raise API_Error(
                    f"Failed to connect to Sentry!",
                    {"dsn": self.settings.sentry.dsn, "error": e},
                    stack_trace=traceback.format_exc()
                )

    
    def _initialize_database(self) -> Optional[MongoDB_Database]:
        ''' Initialize the database by creating passed fixture and 
            indices. Check if the database can be connected to if the
            application requires it. Return the database if it can be connected to
        ''' 
        requires_mongodb = self.settings.flask.requires_mongodb or False

        # Set up database driver
        database = MongoDB_Database(
            settings=self.settings.mongodb,
            indices=self.indices,
            fixtures=self.fixtures,
            connection_must_be_valid=requires_mongodb
        )

        # If MongoDB is not required but the connection is valid, create and return the DB
        if requires_mongodb or database.validate_connection():
            if self.settings.flask.log_boot_events:
                ApplicationLogger.critical(f"[Setting up Database]")

            # Create indices
            if self.indices and len(self.indices):
                database.create_indices()
                ApplicationLogger.warn(
                    f"[Created [{len(self.indices)}] database {'indices' if len(self.indices) > 1 else 'index'}]"
                )

            # Create fixtures
            if self.fixtures and len(self.fixtures):
                database.create_fixtures()
                ApplicationLogger.warn(
                    f"[Created [{len(self.fixtures)}] database fixture{'s' if len(self.fixtures) > 1 else ''}]"
                )

            return database

    def _register_error_handlers(self):
        ''' Register wrappers to handle specific kinds of errors '''
        
        @self.app.errorhandler(API_Error)
        @cross_origin(origins=self.settings.flask.cors_origins, supports_credentials=True)
        def handle_user_thrown_error(error:API_Error):
            sentry_sdk.capture_exception(error)

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