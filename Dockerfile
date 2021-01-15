FROM python:3.8

WORKDIR code

COPY . /code

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

RUN python manage.py collectstatic --noinput
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
