# api_yamdb

## api_yamdb - API для сервиса отзывов yamdb.
REST API для вымышленного сайта ценителей различных произведений искусства yamdb. 
Реализованы: регистрация и аутентификация по JWT токенам, добавление произведений различных категорий и жанров, отзывы и комментарии, модерация. Все это упаковано в контейнеры Docker`а для быстрого развертывания проекта.

Произведения делятся на следующие категории: «Книги», «Фильмы», «Музыка». Администратор может расширить список категорий, а также удалять произведения, категории и жанры, назначать роли пользователям. Зарегистрированные пользователи могут оставлять к произведениям текстовые отзывы и ставить оценку в диапазоне от одного до десяти произведениям, комментировать отзывы. Также они могут редактировать и удалять свои отзывы и комментарии, свои оценки произведений.

Yamdb был написан мной в рамках учебного проекта, целью которого было изучение Django REST Framework и механизмов аутентификации по токенам. База данных на основе PosgreSQL и Django ORM.

Все взаимодействия доступны через API. Используйте следующий URL для ознакомления с возможностями (URL будет автоматически доступен после запуска проекта):
```
redoc/
```

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
- Клонировать репозиторий
- Создать виртуальное окружение и установить зависимости из requirements.txt
- Установить Docker и docker-compose
- Забилдить и поднять проект:
```
$ docker-compose up -d --build 
```
- Выполнить команды для миграции, создания суперюзера и сбора статики:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
- Загрузить список ингредиентов из фикструры:
```
docker-compose exec web python manage.py loaddata ingredients.json
```
- Готово!
