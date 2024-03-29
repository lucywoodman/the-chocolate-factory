from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def index(request):
    """
    A view to return the index page
    """
    context = {"this_is_home": True}
    return render(request, "home/index.html", context)


@require_safe
def privacy(request):
    """
    A view to return the privacy policy page
    """
    return render(request, "home/privacy.html")


@require_safe
def terms(request):
    """
    A view to return the terms & conditions page
    """
    return render(request, "home/terms.html")
