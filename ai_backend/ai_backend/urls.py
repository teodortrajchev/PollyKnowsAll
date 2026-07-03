from django.contrib import admin
from django.urls import path, include

from game import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("game.urls")),
    path("start/", views.start, name="start"),
    path("ask/", views.ask, name="ask"),
    path("", views.index, name="index"),
]