#!/bin/sh

# Exit on error
set -e

echo "Starting entrypoint script..."


# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Load initial data from dump if exists
if [ -f "data_dump.json" ]; then
    echo "Loading initial data from data_dump.json..."
    python manage.py loaddata data_dump.json
fi

# Create or update superuser if environment variables are set
echo "Checking for superuser creation/update..."
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
    username = '$DJANGO_SUPERUSER_USERNAME'; \
    email = '$DJANGO_SUPERUSER_EMAIL'; \
    password = '$DJANGO_SUPERUSER_PASSWORD'; \
    user, created = User.objects.get_or_create(username=username, defaults={'email': email}); \
    user.set_password(password); \
    user.is_superuser = True; \
    user.is_staff = True; \
    user.save(); \
    print('Superuser created/updated successfully.')"
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
