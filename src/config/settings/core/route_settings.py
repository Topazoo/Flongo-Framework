from flask import Flask
from src.config.enums.logs.colors.log_background_colors import LOG_BACKGROUND_COLORS
from src.config.settings.core.app_settings import AppSettings
from src.api.routing.route import Route
from src.utils.logging.loggers.routing import RoutingLogger

class AppRoutes:
    ''' Class that holds all routes for the application
        configured by the user 
    '''

    def __init__(self, *routes: Route) -> None:
        self.routes = routes

    def get_routes(self) -> tuple[Route,...]:
        return self.routes

    def register_routes(self, flask_app:Flask, settings:AppSettings):
        ''' Register all stored routes to a passed app '''

        RoutingLogger().critical(
            RoutingLogger.color_log(f'[Routes Configured]', LOG_BACKGROUND_COLORS.PURPLE)
        )

        for route in self.routes:
            route.register(flask_app, settings)
