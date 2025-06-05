from django.db import models

from api.validators import validate_year


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(
        validators=[validate_year],
        null=True
    )
    genres = models.ManyToManyField(
        'Genre',
        related_name='titles'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.name
