from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# can model be lowercase
# image_link can we take away some of those attributes?
# need to be in uppercase?
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64)
    image_link = models.CharField(max_length=200, default=None, blank=True, null=True)
    seller = models.CharField(max_length=64, default=None)

# model for comments
class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()

class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()
    title = models.CharField(max_length=64, null=True)