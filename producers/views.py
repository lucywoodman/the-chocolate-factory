from django.views import generic
from .models import Producer


class Producers(generic.ListView):
    """A view to return the list of producers"""

    model = Producer
    context_object_name = "producers"
    template_name = "producers/producers.html"
