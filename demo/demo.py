from src.config.settings import AppRoutes, AppSettings
from src.config.settings import FlaskSettings
from src.routing import Route, RouteHandler
from src.responses import API_JSON_Response, API_Error_Response
from src.application import Application

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
            DELETE=lambda request, payload: throw(f'Sample error with payload {payload}'),
            GET=lambda request, payload: "Sample GET request",
            POST=lambda request, payload: API_JSON_Response({'sample_record': '0', 'created': True}, 201),
            PUT=lambda request, payload: API_JSON_Response(9.99)
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
