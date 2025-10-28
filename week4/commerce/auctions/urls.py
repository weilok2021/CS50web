from django.urls import path

from . import views

# My old, messy paths

# urlpatterns = [
#     path("", views.index, name="index"),
#     path("login", views.login_view, name="login"),
#     path("logout", views.logout_view, name="logout"),
#     path("register", views.register, name="register"),
#     path("createlisting", views.create_listing, name="create_listing"),
#     # path("listings/createlisting", views.create_listing, name="create_listing"),
#     path("listings/<int:listing_id>", views.display_listing, name="listing"),
#     # path("closelisting", views.close_listing, name="close_listing"),
#     path("close_listing/<int:listing_id>/", views.close_listing, name="close_listing"),
#     path("listings/Watchlist", views.display_watchlist, name="display_watchlist"),
#     path("listings/<int:listing_id>/AddWatchlist", views.add_watchlist, name="add_watchlist"),
#     path("listings/RemoveWatchlist/<int:watchlist_id>", views.remove_watchlist, name="remove_watchlist"),
#     path("placebid/<int:listing_id>", views.place_bid, name="place_bid"),
#     path("my_listings/", views.my_listings, name="my_listings"),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # Homepage & Authentication
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # Listings
    path("listings/create/", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>/", views.display_listing, name="listing"),
    path("listings/<int:listing_id>/close/", views.close_listing, name="close_listing"),
    path("listings/<int:listing_id>/bid/", views.place_bid, name="place_bid"),

    # Watchlist
    path("watchlist/", views.display_watchlist, name="display_watchlist"),
    path("watchlist/add/<int:listing_id>/", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/<int:watchlist_id>/", views.remove_watchlist, name="remove_watchlist"),

    # User’s own listings (either created or won listings)
    path("my-listings/", views.my_listings, name="my_listings"),
]
