from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms
from django.contrib import messages
from django.shortcuts import redirect
import random

# All of these functions  basically just handle get request, post request or handle both.


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
        "form": NewEntryForm()  # all templates have access to the search form
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

def add_entry(request):
    if request.method == "POST": 
        # extract information from forms input in new_entry.html
        title = request.POST.get("title")
        entry_content = request.POST.get("entry-content")

        if title == None or entry_content == None or title.strip() == "" or entry_content.strip() == "":
            messages.error(request, "Title and content cannot be empty!")
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new_entry.html", {
                "form": NewEntryForm(), # all templates have access to the search form
                "title": title,
                "entry_content": entry_content
            })
        else:
            # check if this entry is existed in the encyclopedia
            for entry in util.list_entries():
                if title.strip().lower() == entry.strip().lower():
                    # When you detect an error:
                    messages.error(request, "An entry with this title already exists!")
                    # Then redirect or render as usual
                    return render(request, "encyclopedia/new_entry.html", {
                        "form": NewEntryForm(), 
                        "title": title,
                        "entry_content": entry_content,
                    })
            
            # save the entry if title and entry content are valid
            # preprocess the title and entry_content into valid format before saving the entry
            # For title - strip whitespace but preserve case?
            title = title.strip()
            # For content - definitely preserve original case
            # entry_content = entry_content.strip()

            # Then save with proper formatting
            util.save_entry(title, f'# {title}\n\n{entry_content}')
            # After util.save_entry(title, entry_content):
            return redirect("display_entry", title=title)

    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm(), # all templates have access to the search form
    })

def random_entry(request):
    rand_entry = random.choice(util.list_entries())
    return display_entry(request, rand_entry)

def edit_entry(request, title):
    # extract current entry content from {title}.md
    curr_entry_content = util.get_entry(title)

    # handle post request
    if request.method == "POST":
        # this is edited content submitted by user
        new_entry_content = request.POST.get("new-entry-content")

        # check if this edited content by user is an invalid input
        # use new_entry_content.strip() == "" to check is new_entry_content is an empty space
        if new_entry_content == None or new_entry_content.strip() == "":
            return render(request, "encyclopedia/new_entry.html", {
                "form": NewEntryForm(), # all templates have access to the search form
                "new_entry_content": new_entry_content, # user should allowed to edit their invalid input
                "title": title,
            })
        else:
            # save the new_entry_content to replace current entry content
            util.save_entry(title, new_entry_content)
            # after saving entry with edited content, redirect user to the entry page
            return redirect("display_entry", title=title)

    # handle get request
    return render(request, "encyclopedia/edit_entry.html", {
        "form": NewEntryForm(), # all templates have access to the search form
        "curr_entry_content": curr_entry_content,
        "title": title,
    })