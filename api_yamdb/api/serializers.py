from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(ModelSerializer):
    """Сериализатор для модели User."""
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'bio', 'role')


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""
    
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre."""
    
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(ModelSerializer):
    """Сериализатор для модели Title."""

    category = CategorySerializer(required=False)
    genre = GenreSerializer(many=True, required=False)
    # rating = 

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    """Сериализатор для модели Review."""

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    """Сериализатор для модели Comment."""

    class Meta:
        model = Comment
        fields = '__all__'
