# Generated by Django 3.2 on 2022-12-20 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование категории', max_length=256, verbose_name='Наименование категории')),
                ('slug', models.SlugField(unique=True, verbose_name='Уникальный идентификатор категории')),
            ],
            options={
                'verbose_name': 'категорию',
                'verbose_name_plural': 'Категории на портале',
            },
        ),
    ]
