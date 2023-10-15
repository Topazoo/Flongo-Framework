#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/app

# Demo can be interchanged with any Python file name with a get_app() binding defined
exec gunicorn "demo.demo:get_app()" -w ${GUNICORN_WORKERS} -b ${APP_HOST}:${APP_PORT} -t ${GUNICORN_TIMEOUT}
