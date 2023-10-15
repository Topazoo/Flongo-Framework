import logging
from ....config.enums.logs.colors import LOG_BACKGROUND_COLORS, LOG_TEXT_COLORS

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': LOG_TEXT_COLORS.BLUE,
        'INFO': LOG_TEXT_COLORS.GREEN,
        'WARNING': LOG_TEXT_COLORS.YELLOW,
        'ERROR': LOG_TEXT_COLORS.RED,
        'CRITICAL': LOG_TEXT_COLORS.PURPLE,
        'APPLICATION': LOG_BACKGROUND_COLORS.PURPLE
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS[record.levelname]}{log_message}{LOG_TEXT_COLORS.END}"
