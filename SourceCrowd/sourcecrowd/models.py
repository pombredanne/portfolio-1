from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.

class User(AbstractUser):
    pass

class Source(models.Model):
    sourcerer = models.ForeignKey(User, on_delete=CASCADE)
    link = models.URLField()
    title = models.TextField(max_length=100)
    description = models.TextField(max_length=280)
    date = models.DateField(auto_now=True)
    clicks = models.IntegerField(default=0)
    votes_count = models.IntegerField(default=0)
    voted_by_user = models.BooleanField(default=False)

class Votes(models.Model):
    source = models.ForeignKey(Source, on_delete=CASCADE)
    voter = models.ForeignKey(User, on_delete=CASCADE)
    vote = models.TextField()

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ForeignKey(Source, on_delete=CASCADE)
