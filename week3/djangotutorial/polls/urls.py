from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index") # define what view will appear at the index/main page
]