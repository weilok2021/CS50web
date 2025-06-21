from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
        Inherits properties such as username, email, password, etc from AbstractUser.
    """
    pass


class Listing(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    starting_price = models.FloatField()
    img_url = models.CharField(max_length=1000)
    # created by who?
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")

    def __str__(self):
        return f"Title: {self.title}, Posted by: {self.creator.username}."

    
class Comment(models.Model):
    # each comment belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

# A general listing is needed for the website
# User listing for it's own, and watchlist of user.