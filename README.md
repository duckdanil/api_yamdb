# Описание проекта YaMDb

Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).  Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

# Используемые технологии

Python 3.7, Django 2.2, Django ORM, Django REST Framework, SQLite3, Simple-JWT

## Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/duckdanil/api_yamdb.git
```
cd api_yamdb
```
- Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
. venv/Scripts/activate
```
- Обновить менеджер пакетов:
python -m pip install --upgrade pip
```
- Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python manage.py migrate
```
- Загрузить тестовую выборку (опционально):
```
python manage.py import_into_db
```
- Запустить проект:
```
python manage.py runserver
```

## Настроены такие эндпоинты:

```
    api/v1/categories/ (GET, PUT, PATCH, DELETE): категории (типы) произведений.
    api/v1/genres/ (GET, PUT, PATCH, DELETE): жанры произведений.
    api/v1/titles/ (GET, PUT, PATCH, DELETE): произведения, к которым пишут отзывы.
    api/v1/titles/{title_id}/reviews/ (GET, PUT, PATCH, DELETE): отзывы на произведения.
    api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, PUT, PATCH, DELETE): комментарии к отзывам.
    api/v1/users/ (GET, PUT, PATCH, DELETE): управление пользователями. 
    api/v1/auth/signup/ (POST): регистрация.
    api/v1/auth/token/ (POST):  получить токен.
    api/v1/users/me/ (GET, PATCH): управление своими пользовательскими данными.
```

## Примеры запросов:
    POST http://127.0.0.1:8000/api/v1/auth/signup/
    Content-Type: application/json

    {
        "username": "user",
        "email": "user@user.ru"
    }

    POST http://127.0.0.1:8000/api/v1/auth/token/
    Content-Type: application/json

    {
        "username": "user",
        "confirmation_code": "Mdgdr..."
    }

    POST http://127.0.0.1:8000/api/v1/categories/
    Authorization: Bearer eyJ0eX...
    Content-Type: application/json

    {
        "name": "Программирование",
        "slug": "programme"
    }

    GET http://127.0.0.1:8000/api/v1/users/
    Authorization: Bearer eyJ0eXAiO...

    GET http://127.0.0.1:8000/api/v1/users/Test/
    Authorization: Bearer eyJ0eXAiO...

    PATCH http://127.0.0.1:8000/api/v1/users/Test/
    Authorization: Bearer eyJ0eXAiO...
    Content-Type: application/json

    {
        "bio": "Я не работаю",
        "role": "user"
    }
    
    http://127.0.0.1:8000/api/v1/users/me/
    Authorization: Bearer eyJ0eXAiO
    Content-Type: application/json

    {
        "bio": "Ничего интересного"
    }
    
```
# Разработчики

[olegtsss](https://github.com/olegtsss): работа с токенами, модели, сериализаторы, админка.
[duckdanil](https://github.com/duckdanil): контроллеры.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
