from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("new/", views.new, name="new"),
    path("random/", views.random, name="random"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>", views.wiki, name="wiki")
]
