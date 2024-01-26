from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    released = models.DateField()
    runtime = models.CharField(max_length=30)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    writers = models.TextField()
    actors = models.TextField()
    plot = models.TextField()
    country = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=500, unique=True)
    
    
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    host = models.ForeignKey(User, related_name='hosted_events', on_delete=models.CASCADE)
    date = models.DateTimeField()
    invitees = models.ManyToManyField(User, related_name='invited_events')
    attendees = models.ManyToManyField(User, related_name='attended_events')
    
class DiscussionBoard(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    moderators = models.ManyToManyField(User, related_name = 'moderated_boards')
    
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, realted_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_comments')