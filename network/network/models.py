from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class User(AbstractUser):
    pass

class Likes(models.Model):
    post_id = models.IntegerField()
    liked_by = models.ForeignKey(User, on_delete=CASCADE)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="poster")
    content = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_by_user = models.BooleanField(default=False)
    allow_edit = models.BooleanField(default=False)

class Followers(models.Model):
    of = models.ForeignKey(User, on_delete=CASCADE, related_name="followers_of")
    followed = models.ForeignKey(User, on_delete=CASCADE, related_name="followers")


class Following(models.Model):
    of = models.ForeignKey(User, on_delete=CASCADE, related_name="followings_of")
    followed = models.ForeignKey(User, on_delete=CASCADE, related_name="following")


    
