from django.core.management.base import BaseCommand
from django.conf import settings
import csv
from reviews.models import Categorie, Genre, Title, GenreTitle

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open((settings.BASE_DIR / 'static/data/category.csv'), 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                Categorie.objects.create(id=row['id'], name=row['name'], slug=row['slug'])

        with open((settings.BASE_DIR / 'static/data/genre.csv'), 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                Genre.objects.create(id=row['id'], name=row['name'], slug=row['slug'])

        with open((settings.BASE_DIR / 'static/data/genre_title.csv'), 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                GenreTitle.objects.create(id=row['id'], genre_id=row['genre_id'], 
                                          title_id=row['title_id']
                                          )

        with open((settings.BASE_DIR / 'static/data/titles.csv'), 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                Title.objects.create(id=row['id'], name=row['name'], year=row['year'], 
                                     category_id=row['category_id']
                                     )

        # with open((settings.BASE_DIR / 'static/data/comments.csv'), 'r') as csv_file:
        #     csv_reader = csv.DictReader(csv_file)
        #     for row in csv_reader:
        #         Comment.objects.create(id=row['id'], review_id=row['review_id'], 
        #                                text=row['text'], author=row['author'], pub_date=row['pub_date'] 
        #                                )

        # with open((settings.BASE_DIR / 'static/data/review.csv'), 'r') as csv_file:
        #     csv_reader = csv.DictReader(csv_file)
        #     for row in csv_reader:
        #         Review.objects.create(id=row['id'], title_id=row['title_id'], 
        #                                text=row['text'], author=row['author'], score=row['score'],
        #                                pub_date=row['pub_date']
        #                                )

        # with open((settings.BASE_DIR / 'static/data/users.csv'), 'r') as csv_file:
        #     csv_reader = csv.DictReader(csv_file)
        #     for row in csv_reader:
        #         User.objects.create(id=row['id'], username=row['username'], email=row['email'],
        #                             role=row['role'], bio=row['bio'], first_name=row['first_name'],
        #                             last_name=row['last_name']
        #                             )
