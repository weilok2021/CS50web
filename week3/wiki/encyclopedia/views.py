from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms

# to create a django form for user to submit rather than the html form
# this will do client validation for us and we can do server validation in views.py
class NewEntryForm(forms.Form):
    entry = forms.CharField(
        label="New Entry",
        widget=forms.TextInput(attrs={
            # html attributes for styling in css
            "class": "search-input",  
            "placeholder": "Search Encyclopedia..."
        })
    )
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewEntryForm()  # all templates have access to the form
    })


def display_entry(request, title):
    title = title.strip().lower() # remove spaces and standardize into lower cases
    entry_content = util.get_entry(title)

    # entry does exists
    if entry_content:
        # # convert markdown to html
        entry_content = util.md_converter(entry_content)

        # pass the entry title and converted entry content(html texts) as the context of entry.html
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry_content": entry_content,
            "form": NewEntryForm()  # all templates have access to the form
        })
    else:
        return HttpResponse("<h1>Page Not Found Error</h1><h2>This entry does not exists in the encyclopedia</h2>")

def search_entry(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the entry from the 'cleaned' version of form data
            entry = form.cleaned_data["entry"]
            entry = entry.strip().lower() # remove spaces and standardize into lower cases

            # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
            if util.get_entry(entry):
                return display_entry(request, entry)

            # else if the entry is not exist, check if there are any related entries in encyclopedia      
            else:
                # check if user entry is the substring of available entries, if so stored the related entry in related_entries
                related_entries = [e for e in util.list_entries() if entry in e.lower()]

                # pass related entries into the context of related.html
                return render(request, "encyclopedia/related.html", {
                    "related_entries": related_entries,
                    "user_entry": entry,
                    "form": NewEntryForm() # reset form after received a submission from user
                })
        elif form.is_valid():
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/related.html", {
                "form": form # all templates have access to the form
            })
    
    
    # when user load the page, a get request will be send to this function, and a new form will be generated for the rendered page
    return render(request, "encyclopedia/index.html", {
        "form": NewEntryForm()
    })
