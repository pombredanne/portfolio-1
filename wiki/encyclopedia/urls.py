from re import search
from django.urls import path

from . import views, util


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="title"),
    path("search", views.search, name="search"),
    path("newpage", views.newPage, name="newPage"),
    path("randompage", views.randomPage, name="randomPage"),
    path("wiki/editpage/<str:title>", views.editPage, name="editPage")
]