# Generated by Django 3.2 on 2022-12-26 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221226_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=64, verbose_name='Код подтверждения для API'),
        ),
    ]
