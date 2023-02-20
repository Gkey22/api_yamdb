from django.contrib.auth import get_user_model 
from django.db import models


User = get_user_model()


class Category(models.Model): 
    name = models.CharField(max_length=256) 
    slug = models.SlugField(max_length=50, unique=True) 
 
    def __str__(self): 
        return self.name 


class Genre(models.Model): 
    name = models.CharField(max_length=256) 
    slug = models.SlugField(max_length=50, unique=True) 
 
    def __str__(self): 
        return self.name


class Title(models.Model): 
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(blank=False)
    description = models.CharField(max_length=256, blank=True) 
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', 
        blank=True, related_name='title_genre'
    )
    categorie = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=False,
        null=True, related_name='title_category'
    )

    def __str__(self): 
        return self.name
    

class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='titles'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genres'
    )
