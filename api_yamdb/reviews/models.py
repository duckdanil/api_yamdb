from django.contrib.auth.models import AbstractUser
from django.db import models


LENGTH_TEXT = 15
MAX_LENGTH_TEXT = 256
GENRES = [
    'Сказка',
    'Рок',
    'Артхаус'
]


class User(AbstractUser):
    """Кастомная модель пользователя"""

    bio = models.TextField(
        'Биография',
        blank=True,
    )


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет разные атрибуты"""

    name = models.CharField(
        'Наименование',
        max_length=MAX_LENGTH_TEXT,
        help_text='Введите наименование'
    )
    slug = models.SlugField(
        'Уникальный slug',
        unique=True,
        max_length=50,
        help_text='Введите уникальный идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('slug',)

    def __str__(self):
        return self.slug[0:LENGTH_TEXT]


class Category(CreatedModel):
    """Категории (типы) произведений"""

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории на портале'


class Genre(CreatedModel):
    """Категории жанров"""

    class Meta:
        verbose_name = 'жанры'
        verbose_name_plural = 'Жанры на портале'


class Title(models.Model):
    """Произведения, к которым пишут отзывы"""

    name = models.CharField(
        'Наименование',
        max_length=MAX_LENGTH_TEXT,
        help_text='Введите наименование'
    )
    year = models.IntegerField(
        blank=True,
        verbose_name='Год',
        help_text='Год в котором было издано произведение'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться произведение'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genres',
        verbose_name='Жанр',
        help_text='Жанр, к которому будет относиться произведение'
    )

    class Meta:
        verbose_name = 'произведению'
        verbose_name_plural = 'Произведения на портале'
        ordering = ('name',)

    def __str__(self):
        return self.name[0:LENGTH_TEXT]


class GenreTitle(models.Model):
    """
    Одно произведение может быть привязано к нескольким жанрам.
    В этой модели будут связаны id жанров и id произведений)
    """
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Жанр",
        help_text='ID жанров'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведения",
        help_text='ID произведений'
    )
    
    class Meta:
        verbose_name = "произведению и жанру"
        verbose_name_plural = "Произведения и жанры на портале"
        ordering = ('name',)

    def __str__(self):
        return f'{self.title} {self.genre}'

    # Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
    # При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
    # При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.
    # Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.