from ....config.enums.logs.log_groups import LOG_GROUPS
from ....utils.logging import StatefulLoggingUtil

class RoutingLogger(StatefulLoggingUtil):
    ''' Logger class for routes and route handling '''

    @property
    def LOGGER_NAME(self):
        name = f"{LOG_GROUPS.ROUTING}"
        if self.url:
            name += f":[{self.url}]"
        if self.method:
            name += f":[{self.method}]"

        return name

    def __init__(self, url:str='', method:str='') -> None:
        self.url = url
        self.method = method
