from .....config.enums.base.base_str_enum import BaseStrEnum

class LOG_TEXT_COLORS(BaseStrEnum):
    """ Log colors supported for the application """

    WHITE = "\x1b[37;20m"
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    GREEN = "\x1b[32;20m"
    BLUE = "\x1b[34;20m"
    PURPLE = "\x1b[35;20m"

    END = "\x1b[0m"
