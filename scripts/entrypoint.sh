#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# celery -A core worker -l info --detach
# daphne -b 0.0.0.0 -p 8000 core.asgi:application
python3 manage.py runserver 0.0.0.0:8000