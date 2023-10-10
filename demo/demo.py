from src.config.enums.logs.log_levels import LOG_LEVELS
from src.config.settings import AppRoutes, AppSettings
from src.config.settings import FlaskSettings
from src.api.routing import Route, RouteHandler
from src.api.responses import API_JSON_Response, API_Message_Response
from src.api.responses.errors import API_Error_Message
from src.application import Application
from datetime import datetime

# Method that throws a sample error
def throw(msg): 
    raise ValueError(msg)

# App config for a simple blog application with user accounts
routes = AppRoutes(
    Route(
        # Route that demonstrates built-in error handling
        url='/error',
        handler=RouteHandler(
            # Custom handlers allow a POST request or a GET request to create different errors
            DELETE=lambda request, payload, collection: throw(f'Sample error with payload {payload}'),
            GET=lambda request, payload, collection: API_Message_Response("Sample GET request"),
            POST=lambda request, payload, collection: API_JSON_Response({'sample_record': f'{payload["_id"]}', 'created': True}, 201),
            PUT=lambda request, payload, collection: API_JSON_Response(datetime.now())
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
        log_level=LOG_LEVELS.DEBUG
    ),
    Route(
        # Route that demonstrates built-in error handling
        url='/sample',
        handler=RouteHandler(
            # Custom handlers allow a POST request or a GET request to create different errors
            POST=lambda request, payload, collection: API_Message_Response(collection.insert_one(payload) if collection != None else 'No collection!'),
            GET=lambda request, payload, collection: API_Message_Response(collection.find_one(payload) if collection != None else 'No collection!')
        ),
        log_level=LOG_LEVELS.DEBUG,
        collection_name='sample'
    ),
)

 # Application settings
settings = AppSettings(
    flask=FlaskSettings(
        env="qa", 
        debug_mode=True, 
        log_level=LOG_LEVELS.DEBUG,
        config_log_level=LOG_LEVELS.DEBUG
    )
)

app = Application(routes=routes, settings=settings)
root_app = app.app
if __name__ == '__main__':
    app.run()
