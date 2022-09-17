from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt

from .models import *

class NewPostForm(forms.Form):
    content = forms.CharField(widget=Textarea, max_length=280, label="New Post")


def index(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            post = Post(user=request.user, content=content)    
            post.save()

    p = Paginator(Post.objects.all().order_by('-timestamp'), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    try:
        for post in posts:
            if post.user == request.user:
                post.allow_edit = True
            try:
                liked = Likes.objects.get(post_id=post.id, liked_by=request.user)
                post.liked_by_user = True
            except Likes.DoesNotExist:
                pass
    except TypeError:
        pass

    return render(request, "network/index.html", {
            "NewPostForm" : NewPostForm(),
            "posts" : posts
        })                


def all_posts(request):
    p = Paginator(Post.objects.all().order_by('-timestamp'), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    try:
        for post in posts:
            if post.user == request.user:
                post.allow_edit = True
            try:
                liked = Likes.objects.get(post_id=post.id, liked_by=request.user)
                post.liked_by_user = True
            except Likes.DoesNotExist:
                pass
    except TypeError:
        pass

    return render(request, "network/posts.html", {
        "posts" : posts
    })


def profile(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    try:
        followers = Followers.objects.filter(of=user).values_list('followed', flat=True)
    except Followers.DoesNotExist:
        followers = None

    try:
        following = Following.objects.filter(of=user).values_list('followed', flat=True)
    except Following.DoesNotExist:
        following = None

    try:
        posts = Post.objects.filter(user=user)
    except Post.DoesNotExist:
        posts = []

    if request.user.id in followers:
        followed = True
    else:
        followed = False

    p = Paginator(Post.objects.filter(user=user).order_by('-timestamp'), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    try:
        for post in posts:
            if post.user == request.user:
                post.allow_edit = True
            try:
                liked = Likes.objects.get(post_id=post.id, liked_by=request.user)
                post.liked_by_user = True
            except Likes.DoesNotExist:
                pass
    except TypeError:
        pass

    return render(request, "network/profile.html", {
        "profile" : user,
        "posts" : posts,
        "followers" : len(followers),
        "following" : len(following),
        "followed" : followed,
        "posts" : posts
    })

@login_required
def following(request):
    try:
        following = Following.objects.filter(of=request.user).values_list('followed', flat=True)
    except Following.DoesNotExist:
        following = []

    posted = []
    for user in following:
        post = Post.objects.filter(user=user).order_by('-timestamp')
        for p in post:
            posted.append(p)
    
    p = Paginator(posted, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    for post in posts:
        if post.user == request.user:
            post.allow_edit = True
        try:
            liked = Likes.objects.get(post_id=post.id, liked_by=request.user)
            post.liked_by_user = True
        except Likes.DoesNotExist:
            pass
    
    return render(request, "network/following.html", {
        "posts" : posts
    })

@login_required
def follow(request, follow, action):
    followed = User.objects.get(username=follow)

    if action == "follow":
        do = Followers(of=followed, followed=request.user)
        do.save()
        do2 = Following(of=request.user, followed=followed)
        do2.save()
        
    else:
        do = Followers.objects.get(of=followed, followed=request.user)
        do.delete()
        do2 = Following.objects.get(of=request.user, followed=followed)
        do2.delete()
        
    followers = Followers.objects.filter(of=followed).values_list('followed', flat=True)
    return JsonResponse({"followers" : len(followers)}, status=200)

@login_required
def like(request, post_id, action):
    likes = Post.objects.get(id=post_id)

    if action == "like":
        like = Likes(post_id=post_id, liked_by=request.user)
        like.save()
        likes.likes += 1
        likes.save()
    
    else:
        unlike = Likes.objects.filter(post_id=post_id, liked_by=request.user)
        unlike.delete()
        likes.likes -= 1
        likes.save()

    return JsonResponse({"likes" : likes.likes}, status=200)
    

@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    post = Post.objects.get(id=post_id)
    if post.user != request.user:
        return JsonResponse({"error": "You are not authorised to edit this post."}, status=400)

    data = json.loads(request.body)
    post.content = data.get("content", "")
    post.save()

    return JsonResponse({"success": "Content saved successfully.", "content": post.content}, status=201)
 

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
