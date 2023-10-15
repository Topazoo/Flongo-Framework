from ....config.enums.logs.log_groups import LOG_GROUPS
from ....utils.logging import StatefulLoggingUtil

class DatabaseLogger(StatefulLoggingUtil):
    ''' Logger class for the database '''

    _BASE_NAME = LOG_GROUPS.DATABASE

    @property
    def LOGGER_NAME(self):
        name = f"{self._BASE_NAME}"
        if self.database:
            name += f":[{self.database}]"
        if self.collection:
            name += f":[{self.collection}]"

        return name

    def __init__(self, database:str='', collection:str='') -> None:
        self.database = database
        self.collection = collection
