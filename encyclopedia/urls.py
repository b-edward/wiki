from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index, name="wiki"),
    path("<str:title>", views.entry, name="entry")
]
