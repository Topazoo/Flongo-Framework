# Flongo Framework

A framework for rapid application development on Flask. Includes:

- Built-in easy HTTP request/response management and error handling
- Built-in query string and response body parsing / normalization
- Built-in request and response payload validation using JSONSchema
- Built-in CORS handling and request origin configuration
- Built-in endpoint permissions handling with cookie-based JWT
- Built-in bindings for MongoDB including fixtures and index management
- Built-in automatic CRUD handling for endpoints given a MongoDB collection name
- Built-in detailed logging and fine-tuneable configurations
- Built-in Sentry integration with detailed spans for request tracing
- Dockerfile/Docker Compose to easily build and run the application

## Sample App

```python
# app
from flongo_framework.application import Application

# routing
from flongo_framework.api.routing import App_Routes, Route, Route_Schema, \
    Route_Handler, Default_Route_Handler, Route_Permissions

# utils
from flongo_framework.utils.jwt import Authentication_Util

# responses
from flongo_framework.api.responses import API_JSON_Response, API_Message_Response
from flongo_framework.api.responses.errors import API_Error_Message, API_Error_Response

# database
from flongo_framework.database.mongodb.index import MongoDB_Indices, MongoDB_Index
from flongo_framework.database.mongodb.fixture import MongoDB_Fixtures, MongoDB_Fixture

# settings
from flongo_framework.config.settings import App_Settings, Flask_Settings, MongoDB_Settings

# enums
from flongo_framework.config.enums.logs.log_levels import LOG_LEVELS

# typing
from typing import Any
from bson import ObjectId
from datetime import datetime


# Method that throws a sample error
def throw(exception_type:type, msg:Any): 
    raise exception_type(msg)

# Simple sample application
routes = App_Routes(
    Route(
        # Route that demonstrates built-in basic request handling
        url='/request',
        handler=Route_Handler(
            GET=lambda request: API_Message_Response("Sample GET request"),
            POST=lambda request: API_JSON_Response({'sample_record': f'{request.payload["_id"]}', 'created': True}, 201),
            PUT=lambda request: API_JSON_Response({'payload': request.payload}),
            DELETE=lambda request: API_JSON_Response({'date': datetime.now(), 'deleted': True}),
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
            GET=lambda request: throw(ValueError, "Oh no! A value error!"),
            POST=lambda request: throw(API_Error_Message, "Oh no! An API error!"),
            PUT=lambda request:  throw(API_Error_Response, {'data': request.payload, 'error': 'Oh no!'}),
        ),
        log_level=LOG_LEVELS.DEBUG
    ),
    Route(
        # Route that demonstrates built-in database handling
        url='/database',
        handler=Route_Handler(
            # Custom handlers allow a POST request or a GET request to create different errors
            POST=lambda request: API_Message_Response(request.collection.insert_one(request.payload) if request.collection != None else 'No collection!'),
            GET=lambda request: API_Message_Response(request.collection.find_one(request.payload) if request.collection != None else 'No collection!')
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
            GET=lambda request: Authentication_Util.set_identity_cookie(
                response=API_Message_Response("Authenticated!"),
                _id="test",
                roles="user"
            ),
            # De-authentication route that removes the JWT in response cookies
            DELETE=lambda request: Authentication_Util.unset_identity_cookie(
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

# Binding directly to Flask for Gunicorn or VSCode
def get_app():
    return app.app

if __name__ == '__main__':
    # Run application
    app.run()
```

## Running With Docker

### Building

From the root directory run:

```sh
docker build -t <your_image_name> -f docker/Dockerfile .
```

### Running

Run the server image on port 8080 from the Docker GUI or with

```sh
docker run -p 8080:8080 <your_image_name>
```

Note: that MongoDB must be configured on the same Docker network as the app **(Use Docker Compose to do this automatically)**

## Running With Docker Compose

Since the server might depend on MongoDB, you can use Docker Compose to start the Dockerized application in conjuction with a Dockerized MongoDB instance

### Building the Server Container

From the docker/ directory containing `docker-compose.yml`, run:

```sh
docker-compose build
```

### Running the Server + MongoDB

From the docker/ directory containing `docker-compose.yml`, run the following to start the server on port 8080 and MongoDB on port 27017:

```sh
docker-compose up --force-recreate
```
