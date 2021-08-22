# YaMDb
### Описание
Проект YaMDb собирает отзывы пользователей на произведения, делящиеся на 3 категории: «Книги», «Фильмы», «Музыка».
### Технологии
Python 3.8.5
Django 3.0.5
### Запуск проекта в dev-режиме
- Соберите контейнеры и запустите их
```
docker-compose up -d --build
```
- Сделайте миграции
```
docker-compose exec web python manage.py migrate --noinput
``` 
- Создайте суперпользователя
```
docker-compose exec web python manage.py createsuperuser
``` 
- Подгрузите статику
```
docker-compose exec web python manage.py collectstatic --no-input
``` 
- Заполните базу начальными данными
``` 
docker-compose exec web python manage.py loaddata fixtures.json 
``` 
### Автор
Ахмед aha252000@mail.ru

![yamdb workflow](https://github.com/gibby25/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
