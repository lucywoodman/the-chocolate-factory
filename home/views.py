from django.shortcuts import render


def index(request):
    """A view to return the index page"""
    context = {"this_is_home": True}
    return render(request, "home/index.html", context)
