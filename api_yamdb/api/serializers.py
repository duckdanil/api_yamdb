from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from django.conf import settings


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

    # category = CategorySerializer(required=False)
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    genre = GenreSerializer(many=True, required=False) 
    rating = serializers.IntegerField(
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

# class RegistrationSerializer(serializers.Serializer, ValidateUsername):
#    """Сериализатор регистрации User"""
#    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
#    email = serializers.EmailField(required=True, max_length=EMAIL)

#class TokenSerializer(serializers.Serializer, ValidateUsername):
#    """Сериализатор токена"""
#    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
#    confirmation_code = serializers.CharField(required=True)


class UserSerializer(ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', 'bio', 'role'
        )