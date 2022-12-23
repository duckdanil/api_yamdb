import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


HELP_MESSAGE = 'Импорт данных из static/data/*.csv'
START_MESSAGE = 'Начинаем импорт...'
STOP_MESSAGE = 'Иморт закончен...'
IMPORT_ERROR = 'Что-то пошло не так: {error}.'
IMPORT_MESSAGE = 'Обрабатывается набор данных: {data}'


def import_into_db_from_csv():
    """Импорт информации из csv файлов в базу данных."""

    # files = []
    # for file in files:
    with open('api_yamdb/static/data/category.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Пропускаем заголовки
        next(reader)
        Category.objects.all().delete()
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            Category.objects.get_or_create(name=row[1], slug=row[2])


class Command(BaseCommand):
    """
    Класс для работы managment комманды.
    python api_yamdb/manage.py import_into_db
    """

    help = HELP_MESSAGE

    def handle(self, *args, **options):
        print(START_MESSAGE)
        try:
            import_into_db_from_csv()
        except Exception as error:
            print(IMPORT_ERROR.format(error=error))

        finally:
            print(STOP_MESSAGE)
