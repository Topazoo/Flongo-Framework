
from typing import Optional

from src.config.settings.app_settings.flask_settings import FlaskSettings
from src.config.settings.app_settings.mongodb_settings import MongoDB_Settings

class AppSettings:
    ''' Class that holds all application settings configured by the user 
    '''

    def __init__(self,
            flask:Optional[FlaskSettings]=None,
            mongo_db:Optional[MongoDB_Settings]=None
        ) -> None:
        
        # Register all created settings or create them
        self.flask = flask or FlaskSettings()
        self.mongodb = mongo_db or MongoDB_Settings()
