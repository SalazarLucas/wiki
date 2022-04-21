from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from . import util
from random import choice
from markdown2 import markdown


def edit(request, title):
    # Allow user to edit a Wiki page
    if request.method == "POST":
        entry_data = request.POST.dict()
        text = entry_data['entry']

        if text:
            util.save_entry(title, text)

        return HttpResponseRedirect(f"/wiki/{title}")

    entry = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "title": title
    })


def index(request):
    # Return index page to user
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def new(request):
    # Allows user to create a new Wiki page.
    if request.method == "POST":
        entry_data = request.POST.dict()
        title = entry_data['title'].capitalize()
        text = entry_data['entry']
        
        if title in util.list_entries():
            messages.error(request, f"There is a page with the title {title} already! You can edit it instead.")
            return render(request, "encyclopedia/new.html")
        
        util.save_entry(title, text)

        return HttpResponseRedirect(f"/wiki/{title}")
    
    return render(request, "encyclopedia/new.html")


def random(request):
    # Redirects user to a random Wiki page.
    entries = util.list_entries()
    return HttpResponseRedirect(f"/wiki/{choice(entries)}")


def search(request):
    # Shows to the user a search results page for a given query.
    entries = util.list_entries()
    query = request.GET.dict()['q']
    search = [entry for entry in entries if query.lower() in entry.lower()]

    if query in entries or not search:
        return HttpResponseRedirect(f"/wiki/{query}")
    
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": search
        })


def wiki(request, title):
    # Shows to the user a Wiki page.
    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown(entry)
        })
    
    return render(request, "encyclopedia/error.html", {
        "title": title
    })
