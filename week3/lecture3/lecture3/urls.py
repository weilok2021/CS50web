from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("myapp/", include("myapp.urls")),
    path("newyear/", include("newyear.urls")),
    path("tasks/", include("tasks.urls")),
]
