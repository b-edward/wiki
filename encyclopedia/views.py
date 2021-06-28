import re
from django.shortcuts import render
from . import util


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
            '''if entry.find(search) == -1:
                matchCount = matchCount
                continue '''
            
            if re.search(search, entry, re.IGNORECASE):
                matches.append(entry)
                matchCount = matchCount + 1

        if matchCount == 0:
            matchCount = 7
            return render(request, "encyclopedia/error.html", {
            "title": title, "matches": matches, "count": matchCount
            })            
        else: 
            return render(request, "encyclopedia/partial.html", {
                "title": title, "matches": matches
                })