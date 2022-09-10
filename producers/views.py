from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from producers.forms import ProducerForm
from .models import Producer


class Producers(generic.ListView):
    """A view to return the list of producers"""

    model = Producer
    context_object_name = "producers"
    template_name = "producers/producers.html"


class AddProducer(UserPassesTestMixin, generic.CreateView):
    """
    A view to display the producer form.
    To add new producers. Restricted to superusers only.
    """

    model = Producer
    form_class = ProducerForm
    success_url = reverse_lazy("producers")

    def test_func(self):
        return self.request.user.is_superuser
