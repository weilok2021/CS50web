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
    # this path is used when user pressed create new page, and this will be the action of the form.
    path("NewPage", views.add_entry, name="add_entry"),
    # this path's action is used when user pressed random page
    path("RandomEntry", views.random_entry, name="random_entry"),
    # views.edit_entry need to have access to the title parameter to have the entry's info(title, content)
    path("EditEntry/<str:title>", views.edit_entry, name="edit_entry"),
]
