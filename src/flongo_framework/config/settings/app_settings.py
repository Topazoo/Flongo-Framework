
from typing import Optional

from flask import current_app, has_app_context

from ...config.settings.base import Settings

from ...config.settings.flask_settings import Flask_Settings
from ...config.settings.jwt_settings import JWT_Settings
from ...config.settings.mongodb_settings import MongoDB_Settings
from ...config.settings.sentry_settings import Sentry_Settings

class App_Settings:
    ''' Class that holds all application settings configured by the user 
    '''

    def __init__(self,
            flask:Optional[Flask_Settings]=None,
            mongodb:Optional[MongoDB_Settings]=None,
            jwt:Optional[JWT_Settings]=None,
            sentry:Optional[Sentry_Settings]=None
        ) -> None:
        
        # Register all passed settings, load from the current Flask app or create them
        self.flask = flask or Flask_Settings.get_settings_from_flask() or Flask_Settings()
        self.mongodb = mongodb or MongoDB_Settings.get_settings_from_flask() or MongoDB_Settings()
        self.jwt = jwt or JWT_Settings.get_settings_from_flask() or JWT_Settings()
        self.sentry = sentry or Sentry_Settings.get_settings_from_flask() or Sentry_Settings()


    @classmethod
    def get_settings_from_flask(cls) -> Optional["App_Settings"]:
        ''' Get the App settings for the current Flask app '''

        if has_app_context():
            return current_app.config.get(Settings.FLASK_SETTINGS_KEY)
