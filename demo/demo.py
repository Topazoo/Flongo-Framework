from src.config.enums.log_levels import LOG_LEVELS
from src.config.settings import AppRoutes, AppSettings
from src.config.settings import FlaskSettings
from src.api.routing import Route, RouteHandler
from src.api.responses import API_JSON_Response, API_Error_Message, API_Error_Response
from src.application import Application
from datetime import datetime

# Method that throws a sample error
def throw(msg): 
    raise API_Error_Message(msg)

# App config for a simple blog application with user accounts
routes = AppRoutes(
    Route(
        # Route that demonstrates built-in error handling
        url='/error',
        handler=RouteHandler(
            # Custom handlers allow a POST request or a GET request to create different errors
            DELETE=lambda request, payload: throw(f'Sample error with payload {payload}'),
            GET=lambda request, payload: "Sample GET request",
            POST=lambda request, payload: API_JSON_Response({'sample_record': f'{payload["_id"]}', 'created': True}, 201),
            PUT=lambda request, payload: API_JSON_Response(datetime.now())
        ),
        request_schema={
            'POST': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    '_id': {'type': 'integer'}
                },
                'required': ['_id']
            }
        },
        log_level=LOG_LEVELS.INFO
    ),
)

 # Application settings
settings = AppSettings(
    flask=FlaskSettings(
        env="qa", 
        debug_mode=True, 
        log_level=LOG_LEVELS.INFO,
        config_log_level=LOG_LEVELS.INFO
    )
)

app = Application(routes=routes, settings=settings)
root_app = app.app
if __name__ == '__main__':
    app.run()
