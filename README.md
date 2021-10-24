# OCR_P9

## Getting Started

Setup project environment with [venv](https://docs.python.org/fr/3/library/venv.html) and [pip](https://pip.pypa.io).

```bash
$ python3 -m venv env
$ source ./env/bin/activate
$ pip install -r ./requirements.txt

$ python manage.py makemigrations
$ python manage.py migrate

$ python manage.py flush # (if necessary)
$ python3 manage.py loaddata fixtures/*
$ python manage.py runserver
```