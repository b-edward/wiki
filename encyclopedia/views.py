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
        matches = [""]
        for entry in entries:
            for j in range(3):
                match = str(entry[j])
                if title == match:
                    matches.append("match")
        if matches[0] == "":
            return render(request, "encyclopedia/error.html", {
            "title": title
            })            
        else: 
            matches.append("test")
            return render(request, "encyclopedia/partial.html", {
                "title": title, "matches": matches
                })