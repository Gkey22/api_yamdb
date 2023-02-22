from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''Пользователь'''

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь")
    ]

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE,
        default=USER
    )
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(
        max_length=36,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    @property
    def is_user(self):
        if self.role == self.USER:
            return True
        else:
            return False

    @property
    def is_moderator(self):
        if self.role == self.MODERATOR:
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.role == self.ADMIN:
            return True
        else:
            return False


class Categorie(models.Model):
    '''Категории'''
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Жанры'''
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Произведения'''
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(blank=False)
    description = models.CharField(max_length=256, blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        blank=False, related_name='title_genre'
    )
    categorie = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL, blank=False,
        null=True, related_name='title_category'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    '''Связывающий класс'''
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='titles'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genres'
    )


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField(verbose_name='Текст отзыва')
    title = models.ForeignKey(Title,
                              verbose_name='Произведение',
                              on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)],
                                verbose_name='Оценка',
                                null=True)
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (models.UniqueConstraint(fields=('title', 'author'),
                                               name='unique_review'),)
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""
    text = models.TextField(max_length=200,
                            verbose_name='Комментарий к отзыву')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
