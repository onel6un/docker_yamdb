from django.db import models
from django.conf import settings


class Category(models.Model):
    '''Модель категорий.'''
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Модель жанров.'''
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    '''Модель отзывов.'''
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Title(models.Model):
    '''Модель произведения(фильм, книга, песня и т.д.).'''
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    year = models.IntegerField()
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenriesOfTitle',
    )

    def __str__(self):
        return self.name


class GenriesOfTitle(models.Model):
    '''Вспомогательная модель для жанров произведения.'''
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE
    )


class Comments(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True)