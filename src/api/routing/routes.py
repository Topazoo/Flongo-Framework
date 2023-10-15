from flask import Flask
from src.config.enums.logs.colors.log_background_colors import LOG_BACKGROUND_COLORS
from src.config.settings.app_settings import App_Settings
from src.api.routing.route import Route
from src.utils.logging.loggers.routing import RoutingLogger

class App_Routes:
    ''' Class that holds all routes for the application
        configured by the user 
    '''

    def __init__(self, *routes: Route) -> None:
        self.routes = routes

    def get_routes(self) -> tuple[Route,...]:
        return self.routes

    def register_routes(self, flask_app:Flask, settings:App_Settings):
        ''' Register all stored routes to a passed app '''

        RoutingLogger().critical(
            RoutingLogger.color_log(f'[Routing Configuration]', LOG_BACKGROUND_COLORS.PURPLE)
        )

        for route in self.routes:
            route.register(flask_app, settings)
