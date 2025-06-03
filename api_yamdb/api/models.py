from django.db import models


class Title(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE, null=False)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.genre
