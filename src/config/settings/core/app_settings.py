
from typing import Optional

from src.config.settings.app_settings.flask_settings import FlaskSettings

class AppSettings:
    ''' Class that holds all application settings configured by the user 
    '''

    def __init__(self,
            flask:Optional[FlaskSettings]=None,
        ) -> None:
        
        # Register all created settings or create them
        self.flask = flask or FlaskSettings()
