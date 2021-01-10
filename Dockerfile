FROM python:3.8

RUN mkdir /foodgram-project

WORKDIR /foodgram-project

COPY . /foodgram-project

RUN pip install --upgrade pip
RUN pip install -r /foodgram-project/requirements.txt

RUN python manage.py collectstatic --noinput