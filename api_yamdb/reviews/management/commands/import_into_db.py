import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


HELP_MESSAGE = 'Импорт данных из static/data/*.csv'
START_MESSAGE = 'Начинаем импорт...'
STOP_MESSAGE = 'Импорт закончен...'
IMPORT_ERROR = 'Что-то пошло не так: {error}.'
IMPORT_MESSAGE = 'Обрабатывается набор данных: {data}'
PATH_TO_CSV_FILES = 'api_yamdb/static/data/'

CATEGORY_FILE = f'{PATH_TO_CSV_FILES}category.csv'
COMMENT_FILE = f'{PATH_TO_CSV_FILES}comments.csv'
GENRE_TITLE_FILE = f'{PATH_TO_CSV_FILES}genre_title.csv'
GENRE_FILE = f'{PATH_TO_CSV_FILES}genre.csv'
REVIEW_FILE = f'{PATH_TO_CSV_FILES}review.csv'
TITLE_FILE = f'{PATH_TO_CSV_FILES}titles.csv'
USER_FILE = f'{PATH_TO_CSV_FILES}users.csv'


def import_to_user(csv_file):
    """Импорт информации из csv файла в модель User."""
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        # Пропускаем заголовки
        next(reader)
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            id, username, email, role, bio, first_name, last_name = row
            User.objects.get_or_create(
                id=id, username=username, email=email, role=role, bio=bio,
                first_name=first_name, last_name=last_name
            )


def import_to_category(csv_file):
    """Импорт информации из csv файла в модель Category."""
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        Category.objects.all().delete()
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            id, name, slug = row
            Category.objects.get_or_create(id=id, name=name, slug=slug)


def import_to_genre(csv_file):
    """Импорт информации из csv файла в модель Genre."""
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        Genre.objects.all().delete()
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            id, name, slug = row
            Genre.objects.get_or_create(id=id, name=name, slug=slug)


def import_to_title(csv_file):
    """Импорт информации из csv файла в модель Title."""
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        Title.objects.all().delete()
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            id, name, year, category_id = row
            category = Category.objects.get(id=category_id)
            Title.objects.get_or_create(
                id=id, name=name, year=year, category=category
            )


def import_to_genre_title(csv_file):
    """Импорт информации из csv файла в модель GenreTitle."""
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        GenreTitle.objects.all().delete()
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            id, title_id, genre_id = row
            GenreTitle.objects.get_or_create(
                id=id, title_id=title_id, genre_id=genre_id
            )


def import_to_review(csv_file):
    """Импорт информации из csv файла в модель Review."""
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        Review.objects.all().delete()
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            id, title_id, text, author_id, score, pub_date = row
            author = User.objects.get(id=author_id)
            Review.objects.get_or_create(
                id=id, title_id=title_id, text=text, author=author,
                score=score, pub_date=pub_date
            )


def import_to_comment(csv_file):
    """Импорт информации из csv файла в модель Comment."""
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        Comment.objects.all().delete()
        for row in reader:
            print(IMPORT_MESSAGE.format(data=row))
            id, review_id, text, author_id, pub_date = row
            author = User.objects.get(id=author_id)
            Comment.objects.get_or_create(
                id=id, review_id=review_id, text=text,
                author=author, pub_date=pub_date
            )


class Command(BaseCommand):
    """
    Класс для работы managment комманды.
    python api_yamdb/manage.py import_into_db
    """

    help = HELP_MESSAGE

    def handle(self, *args, **options):
        print(START_MESSAGE)
        try:
            import_to_user(USER_FILE)
            import_to_category(CATEGORY_FILE)
            import_to_genre(GENRE_FILE)
            import_to_title(TITLE_FILE)
            import_to_genre_title(GENRE_TITLE_FILE)
            import_to_review(REVIEW_FILE)
            import_to_comment(COMMENT_FILE)
        except Exception as error:
            print(IMPORT_ERROR.format(error=error))

        finally:
            print(STOP_MESSAGE)
