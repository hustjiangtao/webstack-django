run:
	.venv/bin/gunicorn django_base.wsgi:application -c ./deploy/gunicorn.conf.py

dev:
	.venv/bin/python manage.py runserver

test:
	.venv/bin/python manage.py test

migrate:
	.venv/bin/python manage.py migrate