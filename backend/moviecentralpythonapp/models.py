from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year
    rated
    released
    runtime
    genre
    director
    actors
    plot
    country
    poster_url