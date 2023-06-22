# api_yamdb - API для сервиса отзывов yamdb.
## Описание:
REST API для вымышленного сайта ценителей различных произведений искусства yamdb. 

Произведения делятся на следующие категории: «Книги», «Фильмы», «Музыка». Администратор может расширить список категорий, а также удалять произведения, категории и жанры, назначать роли пользователям. Зарегистрированные пользователи могут оставлять к произведениям текстовые отзывы и ставить оценку в диапазоне от одного до десяти произведениям, комментировать отзывы. Также они могут редактировать и удалять свои отзывы и комментарии, свои оценки произведений.

Регистрация и аутентификация реализованы с использованием JWT токенам.

Проект упакован в три docker-контейнера.

## Технологии:
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org)
- [Docker](https://www.docker.com)
- [Docker-compose](https://docs.docker.com/compose/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [PosgreSQL](https://www.postgresql.org)
- [Nginx](https://nginx.org/)
- [Gunicorn](https://gunicorn.org)

## Установка и развертывание проекта:
- Клонировать репозиторий, перейти в директорию с проектом:
- Создать виртуальное окружение и установить зависимости из requirements.txt
- Установить Docker и docker-compose
- Cоздать файл с переменными окружения:
```
cd infra
touch .env
nano .env

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- Забилдить и поднять проект:
```
docker-compose up -d --build
```
- Выполнить команды для миграции, создания суперюзера и сбора статики:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
- Заполнить БД из фикстуры:
```
cp fixtures.json container_id:app/fixtures.json
docker-compose exec web python manage.py loaddata fixtures.json
```
- Запустить проект:
```
docker-compose up -d
```
- Используйте следующий URL для ознакомления с возможностями API (URL будет автоматически доступен после запуска проекта):
```
redoc/
```
- Готово!

![example workflow](https://github.com/truth711/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
