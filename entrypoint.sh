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
    python manage.py loaddata data_dump.json || echo "WARNING: Data loading failed, skipping..."
fi

# Create or update superuser if environment variables are set
echo "Checking for superuser creation/update..."
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not username or not password:
    print('Superuser variables not set, skipping sync.')
else:
    print(f'Syncing user: {username}')
    user, created = User.objects.update_or_create(
        username=username, 
        defaults={'email': email, 'is_superuser': True, 'is_staff': True}
    )
    user.set_password(password)
    user.save()
    print(f'Sync complete. Created: {created}. Status: Active.')
EOF

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
