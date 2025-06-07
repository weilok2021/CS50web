from django.urls import path
from . import views

app_name = "tasks" # django will lookup the app_name to search through urls within this app

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
]