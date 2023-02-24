from django.core.management.base import BaseCommand
from django.conf import settings
from django.shortcuts import get_object_or_404
import csv
from reviews.models import (Category, Genre, Title,
                            Comment, Review, User
                            )

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно епрезаписать данные из CSV-файла в sqlite,
сначала удалите файл db.sqlite3.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами, после чего запустите команду
'python manage.py csv_to_sqldb'
"""


class Command(BaseCommand):
    """Импорт данных из csv в DB через модели
    (Category, Genre, Title, GenteTitle, User, Review)
    """
    def handle(self, *args, **options):
        with open((settings.BASE_DIR / 'static/data/category.csv'),
                  'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                Category.objects.create(id=row['id'],
                                        name=row['name'],
                                        slug=row['slug']
                                        )

        with open((settings.BASE_DIR / 'static/data/genre.csv'),
                  'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                Genre.objects.create(id=row['id'],
                                     name=row['name'],
                                     slug=row['slug']
                                     )

        with open((settings.BASE_DIR / 'static/data/titles.csv'),
                  'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                category = Category.objects.get(pk=row['category_id'])
                Title.objects.create(id=row['id'],
                                     name=row['name'],
                                     year=row['year'],
                                     category=category
                                     )

        with open((settings.BASE_DIR / 'static/data/genre_title.csv'),
                  'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                title_obj = get_object_or_404(Title, id=row['title_id'])
                genre_obj = get_object_or_404(Genre, id=row['genre_id'])
                title_obj.genre.add(genre_obj)
                title_obj.save()

        with open((settings.BASE_DIR / 'static/data/users.csv'),
                  'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                User.objects.create(id=row['id'],
                                    username=row['username'],
                                    email=row['email'],
                                    role=row['role'],
                                    bio=row['bio'],
                                    first_name=row['first_name'],
                                    last_name=row['last_name']
                                    )

        with open((settings.BASE_DIR / 'static/data/review.csv'),
                  'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                author = User.objects.get(id=row['author'])
                Review.objects.create(id=row['id'],
                                      title_id=row['title_id'],
                                      text=row['text'],
                                      author=author,
                                      score=row['score'],
                                      pub_date=row['pub_date']
                                      )

        with open((settings.BASE_DIR / 'static/data/comments.csv'),
                  'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                Comment.objects.create(id=row['id'],
                                       text=row['text'],
                                       pub_date=row['pub_date'],
                                       author_id=row['author'],
                                       review_id=row['review_id']
                                       )
