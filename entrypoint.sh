#!/bin/sh

# Exit on error
set -e

echo "Starting entrypoint script..."


# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if environment variables are set
echo "Checking for superuser creation..."
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
    username = '$DJANGO_SUPERUSER_USERNAME'; \
    email = '$DJANGO_SUPERUSER_EMAIL'; \
    password = '$DJANGO_SUPERUSER_PASSWORD'; \
    not User.objects.filter(username=username).exists() and User.objects.create_superuser(username, email, password); \
    print('Superuser check finished.')"
fi

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
