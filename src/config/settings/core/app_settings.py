from src.config.settings import FlaskSettings
from typing import Optional

class AppSettings:
    ''' Class that holds all application settings configured by the user 
    '''

    def __init__(self,
            flask:Optional[FlaskSettings]=None,
        ) -> None:
        
        # Register all created settings or create them
        self.flask = flask or FlaskSettings()
