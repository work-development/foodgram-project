# foodgram-project

![foodgram_workflow](https://github.com/work-development/foodgram-project/workflows/foodgram_workflow/badge.svg)


Адрес сервера, на котором запущен проект
http://130.193.34.19/ и http://178.154.252.39/


## Test User

You can use test user to Login:

Username: test_user

Password: jTzrNb42


## Starting docker-compose:
```
docker-compose up --build
```
## First Start
**For the first launch**, for project functionality, go inside to the container:
```
docker exec web -t -i <WEB CONTAINER ID> bash
```
**Make migrations:**
```
python manage.py migrate
```
**To create a superuser:**
```
python manage.py createsuperuser
```


## Tech Stack
* [Python 3.8.5](https://www.python.org/)
* [Django 3.1.3](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)

## Licence
