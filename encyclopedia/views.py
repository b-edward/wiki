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
    html = util.convert(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "body": html
    })

