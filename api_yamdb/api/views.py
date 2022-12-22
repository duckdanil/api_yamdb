from rest_framework.viewsets import ModelViewSet

from api.serializers import (CategorySerializer, GenreSerializer,
                             GettokenSerializer, ReviewSerializer,
                             SignupSerializer, TitleSerializer)


class CategoryViewSet(ModelViewSet):
    """Работа с категориями."""

    ...
    # serializer_class = CategorySerializer


class GenreViewSet(ModelViewSet):
    """Работа с жанрами."""

    ...
    # serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Работа с произведениями."""

    ...
    # serializer_class = TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Работа с отзывами."""

    ...
    # serializer_class = ReviewSerializer


class CommentViewSet(ModelViewSet):
    """Работа с комментариями."""

    ...
    # serializer_class = CommentSerializer


class UserViewSet(ModelViewSet):
    """
    Работа с пользователями.
    (в том числе работа с GET /users/me/)
    """

    ...
    # serializer_class = UserSerializer


def signup():
    """
    Пользователь отправляет POST-запрос на добавление нового пользователя
    с параметрами email и username. Функция отправляет письмо с кодом
    подтверждения (confirmation_code) на адрес email.
    """

    ...
    # serializer_class = SignupSerializer


def get_token():
    """
    Пользователь отправляет POST-запрос с параметрами
    username и confirmation_code на эндпоинт,
    в ответе на запрос ему приходит token (JWT-токен).
    """
    ...
    # serializer_class = GettokenSerializer
