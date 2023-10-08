from src.routing.route import Route, RouteHandler
from src.application import Application
from src.responses import API_Error_Response

# Method that throws a sample error
def throw(msg): 
    raise API_Error_Response(msg, 500)

# App config for a simple blog application with user accounts
sample_config = {
    'routes': {
        # Sample Error
        'error': Route(
            # Route that demonstrates built-in error handling
            url='/error',
            handler=RouteHandler(
                # Custom handlers allow a POST request or a GET request to create different errors
                POST=lambda request, payload: throw(f'POST - Error from payload {payload}'),
                GET=lambda request, payload: "HELLO",
            )
        ),
    },

    # Application settings
    'settings': {
        # JWT Settings determine if the app uses JWT, what the token lifespan will be and more
        'jwt_settings': {
            'app_use_jwt': True,
            'app_jwt_lifespan': 600,
            'app_permissions': ['USER', 'ADMIN']
        },
        'app_settings': {
            'app_enable_cors': True
        }
    }
}

app = Application(sample_config)
root_app = app.app
if __name__ == '__main__':
    app.run()
