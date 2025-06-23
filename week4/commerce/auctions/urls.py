from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create_listing"),
    # path("listings/createlisting", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.display_listing, name="listing"),
    path("listings/Watchlist", views.display_watchlist, name="display_watchlist"),
    path("listings/<int:listing_id>/AddWatchlist", views.add_watchlist, name="add_watchlist"),
    path("listings/RemoveWatchlist/<int:watchlist_id>", views.remove_watchlist, name="remove_watchlist")
]