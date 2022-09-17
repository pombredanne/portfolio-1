from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
import random
import markdown2
from django.shortcuts import redirect

from . import util

class NewPageForm(forms.Form):
    pageTitle = forms.CharField(label="Title" )
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditPage(forms.Form):
            text = forms.CharField(widget=forms.Textarea, initial='class', label="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    page = util.get_entry(title)
    
    if page == None:
        return render(request, "encyclopedia\error.html")

    else:
        html = markdown2.markdown_path(f"entries/{title}.md")
        return render(request, "encyclopedia/page.html", {
            "page" : html,
            "title" : title
            })
    

def search(request):
    if request.method == "POST":
        q = request.POST['q'].casefold()

        entries = [x.casefold() for x in util.list_entries()]
        search_list = []

        if q in entries:
            q = request.POST['q']
            return redirect('title', title=q)

        else:
            for entry in util.list_entries():
                if (entry.casefold().find(q) != -1):
                    search_list.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "entries": search_list
            })

def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", {
            "form": NewPageForm()
        })

    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pageTitle"].casefold()
            content = form.cleaned_data["content"]

            if title in [x.casefold() for x in util.list_entries()]:
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "error" : "Title already exists. Choose another title."
                })
            
            else:
                title = form.cleaned_data["pageTitle"]
                util.save_entry(title, content)
                return redirect('title', title=title)

def randomPage(request):
    randomPage = random.choice(util.list_entries())
    return redirect('title', title=randomPage)


def editPage(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                "form" : EditPage(initial={'text': content}),
                "title" : title
                })

    else:
        form = EditPage(request.POST)
        if form.is_valid():
            content = form.cleaned_data["text"]
            util.save_entry(title, content)
            return redirect('title', title=title)
    