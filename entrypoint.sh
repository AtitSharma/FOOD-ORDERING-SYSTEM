#!/bin/sh

echo "⏳ Waiting for PostgreSQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done

echo "✅ PostgreSQL is up"

echo "🚀 Applying migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput


echo "📦 Creating admin user"
python manage.py create_admin_user

echo "🔥 Starting Django server..."
exec "$@"