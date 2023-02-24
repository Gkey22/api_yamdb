from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class CustomUser(AbstractUser):
    '''Кастомная модель пользователя'''
    USER_ROLE_USER = 'user'
    USER_ROLE_MODERATOR = 'moderator'
    USER_ROLE_ADMIN = 'admin'

    USER_ROLE_CHOICES = (
        (USER_ROLE_USER, 'Пользователь'),
        (USER_ROLE_MODERATOR, 'Модератор'),
        (USER_ROLE_ADMIN, 'Админ'),
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_USER)
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(
        max_length=50,
        blank=True
    )

    @property
    def is_user(self):
        if self.role == self.USER_ROLE_USER:
            return True
        else:
            return False

    @property
    def is_moderator(self):
        if self.role == self.USER_ROLE_MODERATOR:
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.role == self.USER_ROLE_ADMIN:
            return True
        else:
            return False

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


User = get_user_model()


class Category(models.Model):
    '''Модель категорий'''
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    '''омдель жанров'''
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Модель произведений'''
    name = models.CharField(max_length=256)
    year = models.SmallIntegerField(
        validators=[year_validator]
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Review(models.Model):
    ''''Модель обзоров'''
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1')
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    '''Модель комментариев'''
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='commented')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
