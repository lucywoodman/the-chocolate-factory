from django.shortcuts import render


def index(request):
    """A view to return the index page"""
    context = {"this_is_home": True}
    return render(request, "home/index.html", context)


def privacy(request):
    """A view to return the privacy policy page"""
    return render(request, "home/privacy.html")


def terms(request):
    """A view to return the terms & conditions page"""
    return render(request, "home/terms.html")
