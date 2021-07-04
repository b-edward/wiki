import re
from django.shortcuts import render, redirect
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint

# form for creating a new page entry
class NewPageForm(forms.Form):
    title = forms.CharField(label = "New Title")
    body = forms.CharField(label = "New Body")

# main page to show all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# get the page and display it
def entry(request, title):
    html = util.convert(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(), "body": html
    })

# find a page
def search(request):
    title = request.GET['q']
    if util.convert(title):       
        html = util.convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(), "body": html
        })
  
    if util.convert(title) == False:
        entries = util.list_entries()
        matches = []
        matchCount = 0
        search = title

        for entry in entries:          
            if re.search(search, entry, re.IGNORECASE):
                matches.append(entry)
                matchCount = matchCount + 1

        if matchCount == 0:
            return render(request, "encyclopedia/error.html", {
            "title": title, "message": "Page Not Found."
            })            
        else: 
            return render(request, "encyclopedia/partial.html", {
                "title": title, "matches": matches
                })

#add a new page
def add(request):
    return render(request, "encyclopedia/add.html", {
        "form": NewPageForm()
    })

# save an entry
def save(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():            
            title = form.cleaned_data["title"]
            entries = util.list_entries()
            for entry in entries:
                if entry == form.cleaned_data["title"]:
                    return render(request, "encyclopedia/error.html", {
                    "title": entry, "message": "an encyclopedia entry already exists with the provided title."
                    })       
        
            body = form.cleaned_data["body"]
            util.save_entry(title, body)

            html = util.convert(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title.capitalize(), "body": html
                })

# get an existing page and use it to present a form for editing
def edit(request, entry):
    #editForm = NewPageForm(initial={util.convert(request.get)})
    '''
        return render(request, "encyclopedia/edit.html", {
            "form": NewPageForm()
        })
    '''

    if request.method == "GET":
        title = entry
        content = util.get_entry(title)
        form = NewPageForm({"title": title, "body": content})
        return render(request, "encyclopedia/edit.html", {
            "form": form, "title": title
            })

    form = NewPageForm(request.POST)

    if form.is_valid():
        title = form.cleaned_data.get("title")
        body = form.cleaned_data["body"]
        util.save_entry(title, body)
        html = util.convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(), "body": html
            })

# pick a random entry and return it
def random(request):
    entries = util.list_entries()
    num_entries = len(entries)
    random_entry = entries[randint(0, num_entries - 1)]
    html = util.convert(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry, "body": html
        })

# find an entry from url
def titlepage(request, title):
    if util.convert(title):       
        html = util.convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(), "body": html
        })
  
    else:
        return render(request, "encyclopedia/error.html", {
        "title": title, "message": "Page Not Found."
        })            

