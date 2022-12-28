import datetime as dt

from django.conf import settings
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, Serializer,
                                        SlugRelatedField, ValidationError, RegexField)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, User

REVIEW_EXIST = 'Можно оставить только один отзыв на произведение!'
BAD_USERNAME = 'Нельзя использовать в качестве username {username}!'


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(ModelSerializer):
    """Сериализатор для модели Title."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, required=False, read_only=True)
    rating = IntegerField(
        max_value=settings.MIN_SCORE, min_value=settings.MAX_SCORE,
        required=False
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value < settings.MIN_YEAR_TITLE:
            raise ValidationError(settings.SMALL_YEAR_MESSAGE)
        if value > int(dt.datetime.now().strftime('%Y')):
            raise ValidationError(settings.BIG_YEAR_MESSAGE)
        return value

    def validate_score(self, value):
        if value < settings.MIN_SCORE:
            raise ValidationError(settings.MIN_SCORE_MESSAGE)
        if value > int(dt.datetime.now().strftime('%Y')):
            raise ValidationError(settings.MAX_SCORE_MESSAGE)
        return value


class TitleWriteSerializer(ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(ModelSerializer):
    """Сериализатор для модели Review."""

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message=REVIEW_EXIST
            )
        ]
        read_only_fields = ('title',)


class CommentSerializer(ModelSerializer):
    """Сериализатор для модели Comment."""

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserwithlockSerializer(ModelSerializer):
    """Сериализатор для модели User. Запрещено изменение роли."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class SignupSerializer(Serializer):
    """Сериализатор для функции Signup."""

    username = RegexField(
        r'^[\w.@+-]+',
        max_length=settings.MAX_LENGTH_USERNAME,
        min_length=None, allow_blank=False)
    email = EmailField(
        required=True, max_length=settings.MAX_LENGTH_EMAIL)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(BAD_USERNAME.format(username=value))
        return value


class GettokenSerializer(Serializer):
    """Сериализатор для функции get_token."""

    username = CharField(
        required=True, max_length=settings.MAX_LENGTH_USERNAME)
    confirmation_code = CharField(
        required=True, max_length=settings.CONFIRMATION_CODE_LENGTH
    )
