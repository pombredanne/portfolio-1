from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("saved", views.saved, name="saved"),
    path("profile", views.profile, name="profile"),

    # API Routes 

    path("vote/<str:source_id>/<str:action>", views.vote, name="vote"),
    path("save/<str:source_id>/<str:action>", views.save, name="save"),
    path("delete/<str:source_id>", views.delete, name="delete"),
    path("checksave/<str:source_id>", views.check_save, name="check_save"),
    path("checkvote/<str:source_id>", views.check_vote, name="check_vote"),

    # Link Ping Route
    path("click/<str:source_id>", views.click, name="click")
]