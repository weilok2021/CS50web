from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, title):
    entry = util.get_entry(title)

    # entry does exists
    if entry:
        # # convert md to html
        entry = util.md_converter(entry)

        # pass the entry title and converted entry content(html texts) as the context of entry.html
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
    else:
        return HttpResponse("<h1>Page Not Found Error</h1><h2>This entry does not exists in the encyclopedia</h2>")
