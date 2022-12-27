import random
from smtplib import SMTPResponseException
from string import ascii_lowercase, ascii_uppercase, digits

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action

from api.permissions import AdminOrModeratorOrAuthorOrReadOnly, AdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GettokenSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User
from rest_framework import mixins
from rest_framework import viewsets

EMAIL_SUBJECT = 'Сервис YaMDB ждет подтверждания email'
EMAIL_BODY = (
    'Для подтверждения email воспользуйтесь этим кодом: {code}'
)
SEND_EMAIL = 'Код подтверждения отправлен на почту {email}.'
USERNAME_USED = 'Пользователь {username} уже существует!'
EMAIL_USED = 'Почта {email} используется другим пользователем!'
SEND_EMAIL_ERROR = (
    'Не удалось отправь электронное письмо на {email}. '
    'Код ошибки: {code}. Ошибка: {error}.'
)
SEND_EMAIL_ERROR_JSON = (
    'Не удалось отправить электронное письмо на {email}! '
    'Пользователь {username} не создан!'
)


def send_email_with_confirmation_code(
    email, confirmation_code, add_user_flag, username=''
):
    """
    Сервис YaMDB отправляет письмо с кодом подтверждения
    (confirmation_code) на указанный адрес email.
    """
    try:
        send_mail(
            EMAIL_SUBJECT,
            EMAIL_BODY.format(code=confirmation_code),
            settings.EMAIL_HOST_USER,
            [email, ],
            fail_silently=False,
        )
        if add_user_flag:
            User.objects.create(
                username=username, email=email,
                confirmation_code=confirmation_code
            )
        return Response(
            {'status': SEND_EMAIL.format(email=email)},
            status=status.HTTP_200_OK
        )
    except SMTPResponseException as error:
        print(
            SEND_EMAIL_ERROR.format(
                email=email, code=error.smtp_code, error=error.smtp_error
            )
        )
        return Response(
            {
                'status': SEND_EMAIL_ERROR_JSON.format(
                    email=email, username=username
                )
            },
            status=status.HTTP_400_BAD_REQUEST
        )


def generate_confirmation_code():
    """Генератор кода подтверждения."""
    return (
        ''.join(random.choices(
            ascii_uppercase + digits + ascii_lowercase,
            k=settings.CONFIRMATION_CODE_LENGTH)
        )
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


@api_view(['POST'])
def signup(request):
    """
    Пользователь отправляет POST-запрос на добавление нового пользователя
    с параметрами email и username. Функция отправляет письмо с кодом
    подтверждения (confirmation_code) на адрес email.
    """
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user_exist_flag = User.objects.filter(username=username).exists()
        # Пользователь может быть создан ранее посредством
        # панели администрирования, тогда confirmation_code не будет задан
        if (
            user_exist_flag
            and not User.objects.get(username=username).confirmation_code
        ):
            confirmation_code = generate_confirmation_code()
            user = User.objects.get(username=username)
            user.confirmation_code = confirmation_code
            user.save()
            return send_email_with_confirmation_code(
                email, confirmation_code, False)
        # Пользователь может быть создан ранее посредством API,
        # тогда confirmation_code будет задан
        elif user_exist_flag:
            confirmation_code = User.objects.get(
                username=username).confirmation_code
            return send_email_with_confirmation_code(
                email, confirmation_code, False)
        # Пользователь создается впервые
        else:
            if User.objects.filter(username=username).exists():
                return Response(
                    {'status': USERNAME_USED.format(username=username)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {'status': EMAIL_USED.format(email=email)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            confirmation_code = generate_confirmation_code()
            return send_email_with_confirmation_code(
                email, confirmation_code, True, username
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    """
    Пользователь отправляет POST-запрос с параметрами
    username и confirmation_code на эндпоинт,
    в ответе на запрос ему приходит token (JWT-токен).
    """
    serializer = GettokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(
            User, username=username, confirmation_code=confirmation_code
        )
        return Response(
            {
                'access': str(RefreshToken.for_user(user).access_token)
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
