import re
from django.shortcuts import render, redirect
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewPageForm(forms.Form):
    title = forms.CharField(label = "New Title")
    body = forms.CharField(label = "New Body")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = util.convert(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "body": html
    })

def search(request):
    title = request.GET['q']
    if util.convert(title):       
        html = util.convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title, "body": html
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
            matchCount = 7
            return render(request, "encyclopedia/error.html", {
            "title": title, "message": "Page Not Found."
            })            
        else: 
            return render(request, "encyclopedia/partial.html", {
                "title": title, "matches": matches
                })

def add(request):
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
        
            body = "#" + title + "\n" + form.cleaned_data["body"]
            util.save_entry(title, body)

            html = util.convert(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title, "body": html
                })

        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewPageForm()
        })
