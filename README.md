# foodgram-project

![foodgram_workflow](https://github.com/work-development/foodgram-project/workflows/foodgram_workflow/badge.svg)

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Локальный запуск проекта
1. Склонируйте проект
2. Установите PostgreSQL и в pgAdmin создайте БД с именем foodgram
3. В файле \foodgram\.env в переменную POSTGRES_PASSWORD введите пароль PostgreSQL
4. Создайте виртуальное окружение 
```
python -m venv venv
```
5. Запустите виртуальное окружение
В cmd перейдите в директорию ...\venv\Scripts и выполните команду activate.bat
6. Установите необходимые библиотеки  
```
pip install -r requirements.txt
``` 
7. Сделайте миграции
```
python manage.py makemigrations
python manage.py migrate
```
8. Запустите проект
```
python manage.py runserver
```
9. Для управления проектом создайте суперпользователя
```
python manage.py createsuperuser
```
Теперь по адресу http://127.0.0.1:8000/admin-page/ будет доступен вход в административный раздел сайта

## Запуск проекта на сервере
1. Склонируйте проект
2. Упакуйте файлы в zip файл (foodgram-project.zip)
3. Установите на сервере Docker и docker-compose
4. Установите утилиту для распаковки ZIP
```
sudo apt install unzip
```
5. Перенесите foodgram-project.zip на сервер и распакуйте его. Для этого локально выполните команду в cmd
```
scp foodgram-project.zip логин_сервера@ID_сервера: /home/логин_сервера/foodgram-project
```
И распакуйте этот файл на сервере, для этого перейдите на сервере в директорию /foodgram-project и выполните команду
```
sudo unzip foodgram-project.zip
```
6. Настройти параметры БД. Перейдите /foodgram-project/foodgram и выполните команду
```
sudo nano .env
```
Измените параметры
```
DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
```
7. Добавьте ID сервера в настройки проекта. Для этого в директории на сервере/foodgram-project/foodgram выполните
```
sudo nano settings.py
```
после чего добавьте Ваш ID в список параметра ALLOWED_HOSTS. Затем в директории /foodgram-project/nginx/nginx.conf выполните
```
sudo nano nginx.conf
```
и добавьте в перечень server_name Ваш ID сервера
8. Запустите docker-compose
```
sudo docker-compose up
```
закройте cmd (не останавливая работу сервера)
10. Выполните миграции в контейнере foodgram-project_web. Для этого выполните команду на сервере, зайдя в него вновь 
```
sudo docker container ls -a
```
что бы узнать CONTAINER_ID. Выполните миграции
```
sudo docker exec CONTAINER_ID python manage.py migrate
```
9. Теперь проект будет доступен по URL Вашего ID сервера
10. Для управления проектом создайте суперпользователя
```
sudo docker exec -ti CONTAINER_ID python manage.py createsuperuser
```
Теперь по адресу ID_сервера/admin-page/ будет доступен вход в административный раздел сайта


## Технологии
* [Python 3.8.5](https://www.python.org/)
* [Django 3.1.3](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)

