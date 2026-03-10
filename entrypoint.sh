#!/bin/sh

# Exit on error
set -e

echo "Starting entrypoint script..."


# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
# Use Gunicorn for production, default to port 8000 or $PORT if provided by Render
PORT=${PORT:-8000}
exec gunicorn monportfolio.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --access-logfile -
