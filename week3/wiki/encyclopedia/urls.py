from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # when user enter /wiki into the url, something should be rendered so the main page.
    path("wiki", views.index, name="wiki"),
    # when user enter /wiki/TITLE into the url, this should render the page that displays the content of that encyclopedia entry
    path("wiki/<str:title>", views.display_entry, name="display_entry"),
    # this path is being used when user search for entries, and this will be the action of the form.
    path("search", views.search_entry, name="search_entry"),
]
