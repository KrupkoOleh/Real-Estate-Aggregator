#!/bin/bash

set -e

python manage.py makemigrations dashboard
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000