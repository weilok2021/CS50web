import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown # to convert markdown text to html 


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    """Case-insensitive entry retrieval"""
    _, filenames = default_storage.listdir("entries")  # More readable version
    for filename in filenames:
        if filename.lower() == f"{title.lower()}.md":
            f = default_storage.open(f"entries/{filename}")
            return f.read().decode("utf-8")
    return None


def md_converter(entry):
    """
    convert markdown text to html text using python-markdown2 package
    then return the html
    """
    markdowner = Markdown()
    html = markdowner.convert(entry)
    return html
