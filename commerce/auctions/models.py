from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auctions(models.Model):

    title = models.CharField(max_length=64)
    photo = models.TextField()
    basePrice = models.IntegerField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioned")
    category = models.CharField(max_length=20)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold")
    active = models.BooleanField(null=True)
    highest = models.IntegerField()


class Bidding(models.Model):
    id = models.IntegerField(primary_key=True)
    highest = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.BooleanField()


class Comment(models.Model):
    listing = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.ForeignKey(Auctions, on_delete=models.CASCADE)