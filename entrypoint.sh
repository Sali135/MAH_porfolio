#!/bin/sh

# Exit on error
set -e

# Function to wait for database if using Postgres
if [ "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    # Extract host and port from DATABASE_URL if possible, or use env vars
    # Simpler approach: check if db service is reachable
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "Database started"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
# Use Gunicorn for production, runserver for dev (if specified)
exec gunicorn monportfolio.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-log -
