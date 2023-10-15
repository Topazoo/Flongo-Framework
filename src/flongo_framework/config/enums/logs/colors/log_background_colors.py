from .....config.enums.base.base_str_enum import BaseStrEnum

class LOG_BACKGROUND_COLORS(BaseStrEnum):
    """ Log background colors supported by the application """

    GREY = "\x1b[47;20m"
    CYAN = "\x1b[46;20m"
    YELLOW = "\x1b[43;20m"
    RED = "\x1b[41;20m"
    GREEN = "\x1b[42;20m"
    BLUE = "\x1b[44;20m"
    PURPLE = "\x1b[45;20m"

    END = "\x1b[0m"
