#!/bin/sh

# Wait for postgres
echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Create database if it doesn't exist
PGPASSWORD=$POSTGRES_PASSWORD psql -h $DB_HOST -U $POSTGRES_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
PGPASSWORD=$POSTGRES_PASSWORD psql -h $DB_HOST -U $POSTGRES_USER -c "CREATE DATABASE $DB_NAME"

# Create necessary directories
mkdir -p /app/static/ /app/media/

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start server
exec "$@" 