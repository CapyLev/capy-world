python manage.py migrate
python manage.py collectstatic --no-input

exec gunicorn config.wsgi:application -b 0.0.0.0:6969
