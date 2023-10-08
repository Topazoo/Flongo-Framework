from src.routing.route import Route
from flask import Flask

class AppRoutes:
    ''' Class that holds all routes for the application
        configured by the user 
    '''

    def __init__(self, *routes: Route) -> None:
        self.routes = routes

    def get_routes(self) -> tuple[Route,...]:
        return self.routes
    
    def register_routes(self, app:Flask):
        ''' Register all stored routes to a passed Flask app '''

        for route in self.routes:
            route.register(app)
