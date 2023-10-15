from flask import Flask
from ...config.enums.logs.log_levels import LOG_LEVELS
from ...config.settings.app_settings import App_Settings
from ...api.routing.route import Route
from ...utils.logging.loggers.routing import RoutingLogger

class App_Routes:
    ''' Class that holds all routes for the application
        configured by the user 
    '''

    def __init__(self, *routes: Route) -> None:
        self.routes = routes
        self._configure_logging()

    def get_routes(self) -> tuple[Route,...]:
        return self.routes

    def register_routes(self, flask_app:Flask, settings:App_Settings):
        ''' Register all stored routes to a passed app '''

        if settings.flask.log_boot_events:
            RoutingLogger().critical(f'[Routing Configuration]')

        for route in self.routes:
            route.register(flask_app, settings)

    def _configure_logging(self):
        RoutingLogger().create_logger(LOG_LEVELS.WARN)
