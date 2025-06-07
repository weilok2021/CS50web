from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # set a name for the path can be reuse at anyway if we wanted to refer to this path
    path("<str:name>", views.greet, name="greet")
]