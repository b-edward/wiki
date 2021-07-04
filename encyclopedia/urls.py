from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="wiki"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("random/", views.random, name="random"),
    path("wiki/<str:title>", views.titlepage, name="titlepage"),
]
