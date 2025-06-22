from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



from .models import User, Listing, Comment, Category, Bid

"""
    User who didn't login can only view active listings, and categories of listings
"""


def index(request):
    active_listings = Listing.objects.filter(state=True) # Active listings for whole website, this could be seen by anyone including those without accounts
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def display_listing(request, listing_id):
    active_listings = Listing.objects.filter(state=True) # Active listings for whole website, this could be seen by anyone including those without accounts
    try:
        listing = active_listings.get(id=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
        })
    except:
        return render(request, "auctions/listing.html", {
            "message": "This is not an active listing!",
        })


@login_required
def create_listing(request):
    listings = Listing.objects.all()
    # handle post request
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        img_url = request.POST["img_url"]
        category_name = request.POST["category"] # optional
        
        user = request.user # get the user
        # assign user to creator field it's like letting the user to instantiate this listing object by himself
        listing = Listing(creator=user, title=title, description=description, starting_price=starting_price, img_url=img_url) 

        # Check is this is a valid category name
        if category_name != None and category_name.strip() != "":
            # instantiate the category
            category = Category(name=category_name)
            # save this category into database
            category.save()
            # relate listing to it's foreign key category object (weak relation, deleting the watch list doesn't affect listing existence)
            listing.category = category
        listing.save() # add this new listing to the database
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

        # redirect("listing", listing_id=listing.id)

    # handle get request
    return render(request, "auctions/new_listing.html", {
        "listings": listings,
    })