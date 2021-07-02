from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index, name="wiki"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
]
