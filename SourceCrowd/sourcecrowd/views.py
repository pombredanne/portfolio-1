from email import message
from email.charset import Charset
from os import link
from xml.dom.minidom import CharacterData
from xml.dom.pulldom import CHARACTERS
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *


class NewSourceForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Max. 100 characters', 'size': 30}), max_length=100)
    link = forms.URLField(widget=forms.URLInput(attrs={'value': 'https://', 'size': 30}))
    description = forms.CharField(widget=Textarea(attrs={'placeholder': 'Max. 280 characters','style': "height: 260px; width: 350px"}), max_length=280)

def index(request):
    message = None
    if request.method == "POST":
        form = NewSourceForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            link = form.cleaned_data["link"]
            description = form.cleaned_data["description"]
            
            new_source = Source(sourcerer=request.user, title=title, link=link, description=description)  
            new_source.save()
            message = "Source added successfully!"
        else:
            message = "Invalid URL!"
            
    

    return render(request, "sourcecrowd/index.html", {
        "NewSourceForm" : NewSourceForm(),
        "message" : message
    })

def search(request):
    if request.method == 'GET' and "q" in request.GET:
        q = request.GET["q"]
        if q == "":
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
        
    try:
        sources = Source.objects.filter(title__icontains=q).union(Source.objects.filter(description__icontains=q)).order_by('-votes_count', '-clicks')
        query =  Paginator(sources, 10)
        page = request.GET.get('page')
        results = query.get_page(page)
    except Source.DoesNotExist:
        results = None

    
    return render(request, "sourcecrowd/search.html", {
        "results" : results,
        "query" : q
    })

def new(request):
    try:
        all = Paginator(Source.objects.all().order_by('-id'), 10)
        page = request.GET.get('page')
        results = all.get_page(page)
    except Source.DoesNotExist:
        all = None

    return render(request, "sourcecrowd/new.html", {
        "results" : results
    })

@login_required
def profile(request):
    try:
        source = Paginator(Source.objects.filter(sourcerer=request.user).order_by('-id'), 10)
        page = request.GET.get('page')
        results = source.get_page(page)
    except Source.DoesNotExist:
        results = None
    
    return render(request, "sourcecrowd/profile.html", {
        "results" : results
    })


@login_required
def saved(request):
    try:
        saved = Save.objects.filter(user=request.user).order_by('-id').values_list('source', flat=True)
    except Save.DoesNotExist:
        saved = []
        return render(request, "sourcecrowd/saved.html", {
            "results" : saved
        })
    
    sources = []
    for saves in saved:
        source = Source.objects.get(id=saves)
        sources.append(source)

    source = Paginator(sources, 10)
    page = request.GET.get('page')
    results = source.get_page(page)
    return render(request, "sourcecrowd/saved.html", {
        "results" : results
    })

@login_required
def save(request, source_id, action):
    source = Source.objects.get(id=source_id)

    if action == "save":
        save = Save(user=request.user, source=source)
        save.save()
        button = "Unsave"

    elif action == "unsave":
        saved = Save.objects.get(user=request.user, source=source)
        saved.delete()
        button = "Save"

    return JsonResponse({"button" : button}, status=200)

@login_required
def vote(request, source_id, action):
    source = Source.objects.get(id=source_id)
    
    if action == "up":
        vote = Votes(source=source, voter=request.user, vote=action)
        vote.save()
        source.votes_count += 1
        source.save()
    elif action == "undo_up":
        vote = Votes.objects.get(source=source, voter=request.user)
        vote.delete()
        source.votes_count -= 1
        source.save()
    elif action == "down":
        vote = Votes(source=source, voter=request.user, vote=action)
        vote.save()
        source.votes_count -= 1
        source.save()
    elif action == "undo_down":
        vote = Votes.objects.get(source=source, voter=request.user)
        vote.delete()
        source.votes_count += 1
        source.save()
        
    return JsonResponse({"votes" : source.votes_count}, status=200)

@login_required
def delete(request, source_id):
    try:
        source = Source.objects.get(id=source_id, sourcerer=request.user)
        source.delete()
        delete = "Deleted!"
        return JsonResponse({"done" : delete}, status=200)

    except Source.DoesNotExist:
        return JsonResponse({"done" : "You're not authorized to delete this!"}, status=401)


@login_required
def check_save(request, source_id):
    source = Source.objects.get(id=source_id)

    try:
        saved = Save.objects.get(user=request.user, source=source)
        save = "Unsave"

    except (Save.DoesNotExist, TypeError):
        save = "Save"

    return JsonResponse({"save" : save}, status=200)

@login_required
def check_vote(request, source_id):
    source = Source.objects.get(id=source_id)

    try:
        voted = Votes.objects.get(source=source, voter=request.user)
        vote = voted.vote
    except Votes.DoesNotExist:
        vote = None
    
    return JsonResponse({"vote" : vote}, status=200)

@csrf_exempt
def click(request, source_id):
    clicked = Source.objects.get(id=source_id)
    clicked.clicks += 1
    clicked.save()
    return HttpResponse(None)



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
            return render(request, "sourcecrowd/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sourcecrowd/login.html")


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
            return render(request, "sourcecrowd/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sourcecrowd/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sourcecrowd/register.html")