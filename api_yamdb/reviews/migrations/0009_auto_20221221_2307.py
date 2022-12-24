# Generated by Django 3.2 on 2022-12-21 17:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(blank=True, help_text='Введите оценку произведения', validators=[django.core.validators.MinValueValidator(1, 'Минимальная оценка 1!'), django.core.validators.MaxValueValidator(10, 'Максимальная оценка 10!')], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True, help_text='Введите год, в котором было издано произведение', validators=[django.core.validators.MinValueValidator(1, 'Год не должен быть меньше 1!'), django.core.validators.MaxValueValidator(2022, 'Указать год из будущего не получится!')], verbose_name='Год'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_review'),
        ),
    ]