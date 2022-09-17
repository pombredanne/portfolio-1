
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.all_posts, name="allPosts"),
    path("following", views.following, name="following"),
    path("follow/<str:follow>/<str:action>", views.follow, name="follow"),
    path("like/<str:post_id>/<str:action>", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("<str:username>", views.profile, name="profile")    
] 
