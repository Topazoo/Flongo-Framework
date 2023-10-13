# app
from src.application import Application
# routing
from src.api.routing import Route, RouteHandler, RouteSchema

# responses
from src.api.responses import API_JSON_Response, API_Message_Response
from src.api.responses.errors import API_Error_Message, API_Error_Response

# database
from src.database.mongodb.index import MongoDB_Indices, MongoDB_Index
from src.database.mongodb.fixture import MongoDB_Fixtures, MongoDB_Fixture

# settings
from src.config.settings import AppRoutes, AppSettings, FlaskSettings, MongoDB_Settings

# enums
from src.config.enums.logs.log_levels import LOG_LEVELS

# typing
from typing import Any
from bson import ObjectId
from datetime import datetime

# Method that throws a sample error
def throw(exception_type:type, msg:Any): 
    raise exception_type(msg)

# Simple sample application
routes = AppRoutes(
    Route(
        # Route that demonstrates built-in basic request handling
        url='/request',
        handler=RouteHandler(
            GET=lambda request, payload, collection: API_Message_Response("Sample GET request"),
            POST=lambda request, payload, collection: API_JSON_Response({'sample_record': f'{payload["_id"]}', 'created': True}, 201),
            PUT=lambda request, payload, collection: API_JSON_Response({'payload': payload}),
            DELETE=lambda request, payload, collection: API_JSON_Response({'date': datetime.now(), 'deleted': True}),
        ),
        # Demonstrates HTTP method based schema validation
        request_schema=RouteSchema(
            POST={
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    '_id': {'type': 'integer'}
                },
                'required': ['_id']
            }
        ),
        response_schema=RouteSchema(
            PUT={
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'payload': {'type': 'object'}
                },
                'required': ['payload']
            }
        ),
        log_level=LOG_LEVELS.DEBUG
    ),
    Route(
        # Route that demonstrates built-in basic error handling
        url='/error',
        handler=RouteHandler(
            GET=lambda request, payload, collection: throw(ValueError, "Oh no! A value error!"),
            POST=lambda request, payload, collection: throw(API_Error_Message, "Oh no! An API error!"),
            PUT=lambda request, payload, collection:  throw(API_Error_Response, {'data': payload, 'error': 'Oh no!'}),
        ),
        log_level=LOG_LEVELS.DEBUG
    ),
    Route(
        # Route that demonstrates built-in database handling
        url='/database',
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
        env="local", 
        debug_mode=True, 
        log_level=LOG_LEVELS.DEBUG,
        config_log_level=LOG_LEVELS.DEBUG
    ),
    mongodb=MongoDB_Settings(
        log_level=LOG_LEVELS.DEBUG
    )
)

# Application Database Indices
indices = MongoDB_Indices(
    MongoDB_Index("sample", "name")
)

# Application Database Fixtures
fixtures = MongoDB_Fixtures(
    MongoDB_Fixture("sample", {"_id": ObjectId("652790328c73b750984aee34"), "name": "Peter"})
)

# Create application
app = Application(routes=routes, settings=settings, indices=indices, fixtures=fixtures)
# Binding for flask debugger
root_app = app.app
if __name__ == '__main__':
    # Run application
    app.run()
