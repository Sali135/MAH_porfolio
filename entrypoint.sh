#!/bin/sh

# Exit on error
set -e

echo "Starting entrypoint script..."


# Wait for DB
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

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
    --access-logfile -
