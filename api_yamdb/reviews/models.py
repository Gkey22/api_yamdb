from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False)
    confirmation_code = models.TextField(blank=True)


class Categorie(models.Model): 
    name = models.CharField(max_length=256) 
    slug = models.SlugField(max_length=50,unique=True) 
 
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
    description = models.TextField() 
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', 
        blank=True, related_name='genre_titles'
    )
    category = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL, blank=False,
        null=True, related_name='title_categories'
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
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'], name='unique_genre'
            ),
        ]
