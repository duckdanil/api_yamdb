import datetime as dt

from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, Serializer,
                                        SlugRelatedField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from django.conf import settings
from reviews.models import Category, Comment, Genre, Review, Title, User


REVIEW_EXIST = 'Можно оставить только один отзыв на произведение!'
BAD_USERNAME = 'Нельзя использовать в качестве username {username}'
USERNAME_USED = 'Пользователь {username} уже существует!'
EMAIL_USED = 'Почта {email} используется другим пользователем!'


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(ModelSerializer):
    """Сериализатор для модели Title."""

    category = SlugRelatedField(read_only=True, slug_field='name')
    genre = GenreSerializer(many=True, required=False)
    rating = IntegerField(
        max_value=settings.MIN_SCORE, min_value=settings.MAX_SCORE
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
            'email', 'username', 'first_name', 'last_name', 'bio', 'role'
        )


class SignupSerializer(Serializer):
    """Сериализатор для функции Signup."""

    email = EmailField(max_length=settings.MAX_LENGTH_EMAIL, allow_blank=False)
    username = CharField(
        required=True, max_length=settings.MAX_LENGTH_USERNAME)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(BAD_USERNAME.format(username=value))
        return value
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        if User.objects.get(username=username):
            raise ValidationError(USERNAME_USED.format(username=username))
        if User.objects.get(email=email):
            raise ValidationError(EMAIL_USED.format(email=email))
        user = User.objects.create(**validated_data)
        return user


class GettokenSerializer(ModelSerializer):
    """Сериализатор для функции get_token."""

    username = CharField(
        required=True, max_length=settings.MAX_LENGTH_USERNAME)
    confirmation_code = CharField(required=True)
