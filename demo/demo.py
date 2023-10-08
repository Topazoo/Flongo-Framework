from src.config.settings.core.app_settings import AppSettings
from src.config.settings.core.route_settings import AppRoutes
from src.config.settings.app_settings.flask_settings import FlaskSettings
from src.routing.route import Route, RouteHandler
from src.application import Application
from src.responses import API_Error_Response

# Method that throws a sample error
def throw(msg): 
    raise API_Error_Response(msg, 500)

# App config for a simple blog application with user accounts
routes = AppRoutes(
    Route(
        # Route that demonstrates built-in error handling
        url='/error',
        handler=RouteHandler(
            # Custom handlers allow a POST request or a GET request to create different errors
            POST=lambda request, payload: throw(f'POST - Error from payload {payload}'),
            GET=lambda request, payload: "HELLO",
        )
    ),
)

 # Application settings
settings = AppSettings(
    flask=FlaskSettings(env="qa", debug_mode=True)
)

app = Application(routes=routes, settings=settings)
root_app = app.app
if __name__ == '__main__':
    app.run()
