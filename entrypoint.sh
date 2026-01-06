#!/bin/sh

# Verify that the database is up and running
# Note: In a real-world scenario, you might want to use a wait-for-it script or similar
# but for now, we rely on the healthcheck in docker-compose or just let Django fail and restart.
# However, `depends_on` in docker-compose helps.

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
