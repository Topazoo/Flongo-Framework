from flask import Flask
from src.config.settings.core.app_settings import AppSettings
from src.routing import RouteHandler

class Route:
    ''' Base class that wraps Flasks normal routing allowing us
        to pick up configured parameters like the database to 
        connect to or the permissions required to access the 
        endpoint
    '''

    def __init__(self, url:str, handler:RouteHandler):
        self.url = url
        self.handler = handler
    
    def register(self, flask_app:Flask, settings:AppSettings):
        ''' Registers this URL to a Flask app and binds all supplied
            methods (e.g. GET or POST) specified in the passed RouteHandler
        '''

        self.handler.register_url_methods(self.url, flask_app, settings)
