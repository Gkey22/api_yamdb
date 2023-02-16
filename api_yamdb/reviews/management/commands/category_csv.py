from django.core.management.base import BaseCommand
from django.conf import settings
import csv
from reviews.models import Categorie, Genre, Title

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open((settings.BASE_DIR / 'static/data/category.csv'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                Categorie.objects.create(id=row[0], name=row[1], slug=row[2])

        with open((settings.BASE_DIR / 'static/data/genre.csv'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                Genre.objects.create(id=row[0], name=row[1], slug=row[2])

        with open((settings.BASE_DIR / 'static/data/titles.csv'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                Title.objects.create(id=row[0], name=row[1], year=row[2], category_id=row[3])
