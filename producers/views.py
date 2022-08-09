from django.shortcuts import render


def producers(request):
    """A view to return the producers page"""
    return render(request, "producers/producers.html")
