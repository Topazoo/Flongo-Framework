
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
        
        # Register all passed settings, load from the current Flask app or create them
        self.flask = flask or FlaskSettings.get_settings_from_flask() or FlaskSettings()
        self.mongodb = mongodb or MongoDB_Settings.get_settings_from_flask() or MongoDB_Settings()


    @classmethod
    def get_settings_from_flask(cls) -> Optional["AppSettings"]:
        ''' Get the App settings for the current Flask app '''

        if has_app_context():
            return current_app.config.get('APP_SETTINGS')
