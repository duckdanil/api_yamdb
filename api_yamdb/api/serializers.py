from django.conf import settings
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, Serializer,
                                        SlugRelatedField)

from reviews.models import Category, Comment, Genre, Review, Title, User


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


class ReviewSerializer(ModelSerializer):
    """Сериализатор для модели Review."""

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = '__all__'


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


class GettokenSerializer(ModelSerializer):
    """Сериализатор для функции get_token."""

    username = CharField(
        required=True, max_length=settings.MAX_LENGTH_USERNAME)
    confirmation_code = CharField(required=True)
