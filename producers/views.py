from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from producers.forms import ProducerForm

from .models import Producer


class Producers(generic.ListView):
    """
    A view to return the list of producers
    """

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
        """
        Check if the user is a superuser
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        If user is not a superuser, display a toast message
        """
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")

    def form_invalid(self, form):
        """
        Show toast error message if the form is invalid
        """
        messages.error(
            self.request,
            "Oops, something went wrong! Please double-check the form.",
        )
        return super().form_invalid(form)


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
        """
        Check if the user is a superuser
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        If user is not a superuser, display a toast message
        """
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")

    def form_invalid(self, form):
        """
        Show toast error message if the form is invalid
        """
        messages.error(
            self.request,
            "Oops, something went wrong! Please double-check the form.",
        )
        return super().form_invalid(form)


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
        """
        Check if the user is a superuser
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        If user is not a superuser, display a toast message
        """
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")
