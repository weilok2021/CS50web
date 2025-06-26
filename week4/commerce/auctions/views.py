from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404




from .models import User, Listing, Comment, Category, Bid, Watchlist

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
        listing = active_listings.get(id=listing_id) # get will trigger error when listing is not active
        category = listing.category
        bids = listing.listing_bid.all() # returns all bids in this listing or an empty query set
        current_price = listing.get_current_price()
        watchlist = listing.listing_watchlist.filter(user=request.user).exists() # verify if a user store this listing into their watchlist
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "category": category,
            "watchlist_exist": watchlist,
            "bids": bids,
            "bids_exists": bids.exists(),
            "bids_count": bids.count(),
            "current_price": current_price,
        })
    except:
        # this block of code runs when the listing is not active. It could be 2 cases
        # case 1: the signed in user is the winner

        # listing = Listing.objects.filter(state=False, id=listing_id)
        # if listing.exists(): # this is a valid listing just that being closed which shows there's a winner
        #     if listing.winner == request.user:
        #         return HttpResponse("Congratulations! You have won the Bid")

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


@login_required
def display_watchlist(request):
    # display watchlist for each signed in user
    all_watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "all_watchlist": all_watchlist,
    })


@login_required
def add_watchlist(request, listing_id):
    # handle post request
    if request.method == "POST":
        # check if this listing already in this user's watchlist
        # get all the user's watchlist
        all_watchlist = Watchlist.objects.filter(user=request.user)
        # be careful what is an empty object represents, empty data for a model != None but is a <QuerySet []>
        if all_watchlist.exists(): # check if watchlist exists in existing watchlist
            for watchlist in all_watchlist:
                if watchlist.listing.id == listing_id: # if listing already existed within watchlist
                    # rerender listing.html with message
                    # render page with some information to tell user shouldn't as this listing already in watchlist
                    messages.warning(request, "This item is already in your watchlist!")
                    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
                
        # if the watchlist is not existed (empty), or listing is not existing within watchlist, add the watchlist.
        listing = Listing.objects.get(id=listing_id) # instantiate this watch list and relate it to user and this listing
        watchlist = Watchlist(user=request.user, listing=listing)
        watchlist.save() # add this into database
        return HttpResponseRedirect(reverse("display_watchlist"))

    # handle get request
    return display_listing(request, listing_id)


@login_required
def remove_watchlist(request, watchlist_id):
    if request.method == "POST":
        watchlist = get_object_or_404(Watchlist, id=watchlist_id)
        # watchlist = Watchlist.objects.get(id=watchlist_id)
        watchlist.delete()
        # redirect to watchlist page after watchlist being removed
        messages.success(request, "Removed from watchlist!")
        return HttpResponseRedirect(reverse("display_watchlist"))
    # handle get request
    return display_watchlist(request)


@login_required
def place_bid(request, listing_id):
    # even invalid bids get save, need to reconsider how to refactor maybe
    # the problems could falls within listing.get_current_price()

    if request.method == "POST":
        price = float(request.POST["price"])
        if price > Listing.objects.get(id=listing_id).get_current_price():
            bid = Bid(user=request.user, listing=Listing.objects.get(id=listing_id), price=price) # the verification will be done within bid model
            bid.save()
        else:
            return HttpResponse("This is not a valid bid! (Please place bid higher than the current price)")
    # handle get request
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id, creator=request.user)
    if listing.exists():
        bids = listing.listing_bid.all()
        if bids.exists():
            highest_bid = bids.order_by("-price").first()
            winner = highest_bid.user
        listing.state = False # close the listing
        listing.winner = winner
        listing.save()
    return HttpResponseRedirect(reverse("index"))

    
    


