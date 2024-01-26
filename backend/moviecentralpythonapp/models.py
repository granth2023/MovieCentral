from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ... your model definitions ...


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
    
    
class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    class Meta(AbstractUser.Meta): 
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
    
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='hosted_events', on_delete=models.CASCADE)
    date = models.DateTimeField()
    invitees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='invited_events')
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attended_events')
    location = models.CharField(max_length=200, null=True, blank=True)
    virtual_event_link=models.URLField(max_length=500, null=True, blank=True)
    
class DiscussionBoard(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'moderated_boards')
    
class Comment(models.Model):
    discussion_board = models.ForeignKey(DiscussionBoard, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')])