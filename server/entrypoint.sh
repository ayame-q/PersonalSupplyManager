#!/bin/sh

python manage.py migrate --noinput

if ! isTrue "$DEBUG"; then
  exec python3 manage.py runserver 0.0.0.0:8000
else
  python manage.py collectstatic --noinput --clear
  exec "$@"
fi