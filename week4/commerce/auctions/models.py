from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# Data logic:
    # (listing existence relies upon User):
        # User might create a listing,
        # User might close a listing created by themselve

    # User might add any active listing to their Watchlist (Watchlist existence relies upon User or Listing)
    # User might post comment on any active listing (Comment existence relies upon User or Listing)
    # User might make a bid on a Listing (Bid existence relies upon User or Listing)

class User(AbstractUser):
    """
        Inherits properties such as username, email, password, etc from AbstractUser.
    """


class Category(models.Model):
    name = models.CharField(max_length=100)


class Listing(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    starting_price = models.FloatField()
    img_url = models.CharField(max_length=1000)
    state = models.BooleanField(default=True) # true denotes active, false denotes no longer active
    # created by who?
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    time = models.DateTimeField(auto_now_add=True)  # Essential for "posted X ago"
    # simplify the use case, each listing belongs to only one category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings") 
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_auctions")

    def get_current_price(self):
        """
            if there are no bids, this function will return the starting price,
            if there are bids, this functino will return the highest bid price. 
            Therefore, this function returns the highest/current price within the listing
        """
        # if there are some bids within this listing
        bids = self.listing_bid.all()
        if bids.exists():
            # get the bid object with highest price
            highest_bid = bids.order_by("-price").first()
            return highest_bid.price
        # else, there are no bids and starting price is current highest price
        return self.starting_price

    # to check if the listing is active
    def is_active(self):
        return self.state

    def __str__(self):
        return f"Title: {self.title}, Posted by: {self.creator.username}."


class Comment(models.Model):
    # each comment belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    # each bid belongs to a user, and a listing
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid")
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)  # Essential for "posted X ago"

    def clean(self):
        """
            django automatically calls clean when I save a model or validate a form.
            Basically to check is this a valid bid
        """
        # A valid bid should be larger than existing bids price or as large as starting price
        # starting_price <= existing_bids.price < valid bid
        highest_price = self.listing.get_current_price()
        # if highest_price == self.listing.starting_price:
        #     pass
        if self.price <= highest_price:
            raise ValidationError(f"Bid must be higher than ${highest_price}")
            

class Watchlist(models.Model):
    # each bid belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watchlist")

    # metadata configuration
    class Meta:
        # A unique combination setting to avoid user adding duplicate listing to the watchlist
        unique_together = ('user', 'listing')