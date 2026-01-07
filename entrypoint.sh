#!/bin/sh

# Verify that the database is up and running
# Note: In a real-world scenario, you might want to use a wait-for-it script or similar
# but for now, we rely on the healthcheck in docker-compose or just let Django fail and restart.
# However, `depends_on` in docker-compose helps.
wait_for_db() {
  echo "Waiting for database to become available..."

  DB_HOST=$(python3 -c "import os; from urllib.parse import urlparse; u=urlparse(os.environ['DATABASE_URL']); print(u.hostname)")
  DB_PORT=$(python3 -c "import os; from urllib.parse import urlparse; u=urlparse(os.environ['DATABASE_URL']); print(u.port or 5432)")

  while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" > /dev/null 2>&1; do
    sleep 1
  done
  echo "Database is available!"
}

echo "Collecting static files..."
python manage.py collectstatic --noinput

if echo "$@" | grep -q "gunicorn"; then
    wait_for_db
    echo "Running database migrations..."
    python manage.py migrate
    echo "Starting Gunicorn..."
fi

echo "Seeding database..."
python manage.py seed_quizzes
python manage.py seed_revisions

exec "$@"

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
