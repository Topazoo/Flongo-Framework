from ....config.enums.base.base_str_enum import BaseStrEnum

class LOG_GROUPS(BaseStrEnum):
    """ Log groups supported by the application """

    ROOT = 'root'
    APP = 'app'
    APP_CONFIG = 'config'
    DATABASE = 'database'
    ROUTING = 'routing'
