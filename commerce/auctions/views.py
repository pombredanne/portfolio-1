from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import *

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput, label="Comment")

class ListForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput, label="Title")
    description = forms.CharField(widget=forms.TextInput, label="Description")
    bid = forms.CharField(widget=forms.TextInput, label="Price")
    photo = forms.CharField(widget=forms.TextInput, label="Image URL")
    category = forms.CharField(widget=forms.TextInput, label="Category")

def index(request):
    if request.method == "POST":
        listing = Auctions.objects.get(id=request.POST["id"])
        listing.active = False
        listing.winner = User.objects.get(username=request.POST["bidder"])
        print(listing.winner)
        listing.save()
        return render(request, "auctions/index.html", {
            "listings" : Auctions.objects.filter(active=True)
        })
    
    return render(request, "auctions/index.html", {
        "listings" : Auctions.objects.filter(active=True)
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            basePrice = int(form.cleaned_data["bid"])
            photo = form.cleaned_data["photo"]
            category = form.cleaned_data["category"]
            user = request.user

            listing = Auctions(title=title, basePrice=basePrice, photo=photo, description=description, owner=user, category=category, active=True, highest=basePrice, winner=user)

            listing.save()

            bidding = Bidding(id=listing.id, highest=basePrice, bidder=user, started=False)

            bidding.save()

            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


    else:
        return render(request, "auctions/create.html",{
            "listForm" : ListForm()
        })

def listing(request, auction_id):
    message = ""
    if request.method == "POST":

        if 'commenting' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data["comment"]
                user = request.user
                listing = Auctions.objects.get(id=auction_id)
                addComment = Comment(listing=listing, user=user, comment=comment)
                addComment.save()

        else:
            listing = Auctions.objects.get(id=auction_id)
            newBid = int(request.POST["newBid"])

            if newBid > listing.highest:
                listing.highest = newBid
                listing.save()
                bidding = Bidding.objects.get(id=auction_id)
                bidding.highest = newBid
                bidding.bidder = request.user
                bidding.started = True
                bidding.save()
                message = "Your bid was placed successfully."

            else:
                message = "Your bid must be greater than the current bid."

    listing = Auctions.objects.get(id=auction_id)
    bidding = Bidding.objects.get(id=auction_id)
    comments = Comment.objects.filter(listing=listing)

    try:
        watchlist = Watchlist.objects.get(user=request.user, added=listing)
    except Watchlist.DoesNotExist:
        watchlist = None
    except TypeError:
        watchlist = None;

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "bidding" : bidding,
        "watchlist" : watchlist,
        "comments" : comments,
        "message" : message,
        "commentForm" : CommentForm()
    })

@login_required
def watchlist(request):
    
    if request.method == "POST":
        listing = Auctions.objects.get(id=request.POST["id"])
        
        if request.POST["action"] == "add":
            add = Watchlist(user=request.user, added=listing)
            add.save()

        else:
            remove = Watchlist.objects.filter(user=request.user, added=listing)
            remove.delete()

    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings" : watchlist
    })

def categories(request):
    categories = Auctions.objects.all()

    return render(request, "auctions/categories.html", {
        "categories" : categories
    })

def category(request, category):
    listings = Auctions.objects.filter(category=category, active=True)

    return render(request, "auctions/category.html", {
        "listings" : listings,
        "category" : category
    })