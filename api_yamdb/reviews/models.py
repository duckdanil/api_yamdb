from django.contrib.auth.models import AbstractUser
from django.db import models


LENGTH_TEXT = 15

class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет разные атрибуты."""

    name = models.CharField(
        'Наименование',
        max_length=256,
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


class Category(CreatedModel):
    """Категории (типы) произведений"""

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории на портале'


class Genry(CreatedModel):
    """Категории жанров"""

    class Meta:
        verbose_name = 'жанры'
        verbose_name_plural = 'Жанры на портале'
