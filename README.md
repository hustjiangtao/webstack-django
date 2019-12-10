# django-base
Django base

## Intro

Basic config for django, including:

- env
- mysql
- deploy setting gunicorn & nginx & supervisor

## Usage

- clone this project

```bash
git clone https://github.com/hustjiangtao/django-base.git django_api
cd django_api
pyenv local 3.6.5
python -m venv .venv
.venv/bin/pip install -r requirements.txt
make dev
```

- add new app

```bash
python manage.py startapp demo
```

- sql migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

- test

```bash
make test
```
