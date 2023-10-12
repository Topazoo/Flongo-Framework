
from typing import Optional

from flask import current_app, has_app_context

from src.config.settings.app_settings.flask_settings import FlaskSettings
from src.config.settings.app_settings.mongodb_settings import MongoDB_Settings

class AppSettings:
    ''' Class that holds all application settings configured by the user 
    '''

    def __init__(self,
            flask:Optional[FlaskSettings]=None,
            mongodb:Optional[MongoDB_Settings]=None
        ) -> None:

        # Attempt to get the settings from a currently
        # running Flask app if instantiated from within
        # the app
        flask_settings = self.get_settings_from_flask()
        if flask_settings:
            flask = flask or flask_settings.flask
            mongodb = mongodb or flask_settings.mongodb
        
        # Register all created settings or create them
        self.flask = flask or FlaskSettings()
        self.mongodb = mongodb or MongoDB_Settings()


    @classmethod
    def get_settings_from_flask(cls) -> Optional["AppSettings"]:
        ''' Get the App settings for the current Flask app '''

        if has_app_context():
            return current_app.config.get('APP_SETTINGS')
