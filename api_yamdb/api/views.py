from api.permissions import AdminOrModeratorOrAuthorOrReadOnly, AdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GettokenSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleSerializer)
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Category, Genre, Review, Title, User


EMAIL_THEME = 'Сервис YaMDB ждет подтверждания email'
EMAIL_BODY = 'Для подтверждения email воспользуйтесь этим кодом: {code}'


def send_email_with_confirmation_code(email, confirmation_code):
    """
    Сервис YaMDB отправляет письмо с кодом подтверждения
    (confirmation_code) на указанный адрес email.
    https://docs.djangoproject.com/en/4.1/topics/email/
    Для тестирования эмулятора:
    from django.conf import settings
    import api.views
    from api.views import send_email_with_confirmation_code
    send_email_with_confirmation_code('first_user@yandex.ru', '12345')
    """
    send_mail(
        EMAIL_THEME,
        EMAIL_BODY.format(code=confirmation_code),
        settings.EMAIL_HOST_USER,
        [email, ],
        fail_silently=False,
    )


class ModelMixinSet(CreateModelMixin, ListModelMixin,
                    DestroyModelMixin, GenericViewSet):
    """Сборный миксин сет"""
    pass


class CategoryViewSet(ModelViewSet):
    """Работа с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(ModelViewSet):
    """Работа с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )


class TitleViewSet(ModelViewSet):
    """Работа с произведениями."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )


class ReviewViewSet(ModelViewSet):
    """Работа с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrModeratorOrAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Работа с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (AdminOrModeratorOrAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


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
