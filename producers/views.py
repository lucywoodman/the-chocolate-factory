from django.shortcuts import redirect
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from producers.forms import ProducerForm
from .models import Producer


class Producers(generic.ListView):
    """A view to return the list of producers"""

    model = Producer
    context_object_name = "producers"
    template_name = "producers/producers.html"


class AddProducer(
    UserPassesTestMixin, SuccessMessageMixin, generic.CreateView
):
    """
    A view to display the producer form.
    To add new producers. Restricted to superusers only.
    """

    model = Producer
    form_class = ProducerForm
    success_message = "Successfully added producer!"
    success_url = reverse_lazy("producers")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")


class UpdateProducer(
    UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView
):
    """
    A view to display the producer form.
    To update producers. Restricted to superusers only.
    """

    model = Producer
    form_class = ProducerForm
    success_message = "Successfully updated producer!"
    success_url = reverse_lazy("producers")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")


class DeleteProducer(
    UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView
):
    """
    A view to delete producers.
    Restricted to superusers only.
    """

    model = Producer
    template = "producers/producers.html"
    success_message = "Successfully deleted producer!"
    success_url = reverse_lazy("producers")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")
