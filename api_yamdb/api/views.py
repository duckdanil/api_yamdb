from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    """Работа с категориями."""
    ...


class GenreViewSet(ModelViewSet):
    """Работа с жанрами."""
    ...


class TitleViewSet(ModelViewSet):
    """Работа с произведениями."""
    ...


class ReviewViewSet(ModelViewSet):
    """Работа с отзывами."""
    ...


class CommentViewSet(ModelViewSet):
    """Работа с комментариями."""
    ...


def signup():
    """
    Пользователь отправляет POST-запрос на добавление нового пользователя
    с параметрами email и username. Функция отправляет письмо с кодом подтверждения
    (confirmation_code) на адрес email.
    """
    ...

def token():
    """
    Пользователь отправляет POST-запрос с параметрами
    username и confirmation_code на эндпоинт,
    в ответе на запрос ему приходит token (JWT-токен).
    """
    ...

def me():
    """
    При желании пользователь отправляет сюда PATCH-запрос и
    заполняет поля в своём профайле (описание полей — в документации)
    """
    ...

def users():
    """Работа с пользователями."""
    ...
