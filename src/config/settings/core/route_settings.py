from flask import Flask
from src.config.settings.core.app_settings import AppSettings
from src.routing.route import Route

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

        for route in self.routes:
            route.register(flask_app, settings)
