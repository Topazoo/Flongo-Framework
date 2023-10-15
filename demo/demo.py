# app
from src.application import Application
# routing
from src.api.routing import App_Routes, Route, Route_Schema, \
    Route_Handler, Default_Route_Handler, Route_Permissions

# responses
from src.api.responses import API_JSON_Response, API_Message_Response
from src.api.responses.errors import API_Error_Message, API_Error_Response

# database
from src.database.mongodb.index import MongoDB_Indices, MongoDB_Index
from src.database.mongodb.fixture import MongoDB_Fixtures, MongoDB_Fixture

# settings
from src.config.settings import App_Settings, Flask_Settings, MongoDB_Settings

# enums
from src.config.enums.logs.log_levels import LOG_LEVELS

# typing
from typing import Any
from bson import ObjectId
from datetime import datetime

from src.utils.jwt.jwt_manager import App_JWT_Manager

# Method that throws a sample error
def throw(exception_type:type, msg:Any): 
    raise exception_type(msg)

# Simple sample application
routes = App_Routes(
    Route(
        # Route that demonstrates built-in basic request handling
        url='/request',
        handler=Route_Handler(
            GET=lambda request, payload, collection: API_Message_Response("Sample GET request"),
            POST=lambda request, payload, collection: API_JSON_Response({'sample_record': f'{payload["_id"]}', 'created': True}, 201),
            PUT=lambda request, payload, collection: API_JSON_Response({'payload': payload}),
            DELETE=lambda request, payload, collection: API_JSON_Response({'date': datetime.now(), 'deleted': True}),
        ),
        # Demonstrates HTTP method based schema validation
        request_schema=Route_Schema(
            POST={
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    '_id': {'type': 'integer'}
                },
                'required': ['_id']
            }
        ),
        response_schema=Route_Schema(
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
        handler=Route_Handler(
            GET=lambda request, payload, collection: throw(ValueError, "Oh no! A value error!"),
            POST=lambda request, payload, collection: throw(API_Error_Message, "Oh no! An API error!"),
            PUT=lambda request, payload, collection:  throw(API_Error_Response, {'data': payload, 'error': 'Oh no!'}),
        ),
        log_level=LOG_LEVELS.DEBUG
    ),
    Route(
        # Route that demonstrates built-in database handling
        url='/database',
        handler=Route_Handler(
            # Custom handlers allow a POST request or a GET request to create different errors
            POST=lambda request, payload, collection: API_Message_Response(collection.insert_one(payload) if collection != None else 'No collection!'),
            GET=lambda request, payload, collection: API_Message_Response(collection.find_one(payload) if collection != None else 'No collection!')
        ),
        log_level=LOG_LEVELS.DEBUG,
        collection_name='sample'
    ),
    Route(
        # Route that demonstrates built-in default CRUD handling
        url='/default',
        handler=Default_Route_Handler(),
        log_level=LOG_LEVELS.DEBUG,
        collection_name='default'
    ),
    Route(
        # Route that demonstrates built-in permissions handling
        url='/permissions',
        handler=Default_Route_Handler(
            # Authentication route that sets the JWT in response cookies
            GET=lambda request, payload, collection: App_JWT_Manager.add_response_jwt(
                response=API_Message_Response("Authenticated!"),
                _id="test",
                roles="user"
            ),
            # De-authentication route that removes the JWT in response cookies
            DELETE=lambda request, payload, collection: App_JWT_Manager.remove_response_jwt(
                response=API_Message_Response("Logged out!"),
            )
        ),
        log_level=LOG_LEVELS.DEBUG,
        collection_name='permissions',
        permissions=Route_Permissions(POST='user', PUT='admin')
    ),
)

 # Application settings
settings = App_Settings(
    flask=Flask_Settings(
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
