#!/bin/bash

mkdir -p /tmp/src

echo "Activating the virtual envs"
. ./src-env/bin/activate

echo "Install the required packages"
pipenv install --dev

echo "Running the migration files"
flask db upgrade

echo "Start celery worker (with Celery beat)"
celery -A src_api.celery_app.celery worker -B -E -D -n worker1@src
celery -A src_api.celery_app.celery worker -B -E -D -n worker2@src
celery -A src_api.celery_app.celery worker -B -E -D -n worker3@src

echo "Starting the service up using dev server"
# flask run --host=0.0.0.0
gunicorn --bind=0.0.0.0:5000 --workers 3 --worker-class gevent --log-level=info src_api:app
