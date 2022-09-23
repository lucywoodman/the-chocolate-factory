from checkout.models import OrderDetail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.text import Truncator
from django.views import generic
from django.views.decorators.http import require_safe

from .forms import ProfileForm, UserForm
from .models import Profile


class UpdateProfile(
    LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    """
    A view to display the profile form.
    To update the user's profile. Restricted to the request user only.
    """

    model = Profile
    form_class = UserForm
    second_form_class = ProfileForm
    success_message = "Profile updated successfully!"
    template_name = "profiles/profile.html"

    def get_object(self, *args, **kwargs):
        """
        Ensures that the logged in user can only see their own profile
        """
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """
        Handle the form context
        """
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        if self.request.POST:
            context["user_form"] = self.form_class(
                self.request.POST, instance=self.request.user
            )
            context["profile_form"] = self.second_form_class(
                self.request.POST, instance=self.object
            )
        else:
            context["user_form"] = self.form_class(instance=self.request.user)
            context["profile_form"] = self.second_form_class(
                instance=self.object
            )
        context["orders"] = self.request.user.profile.orders.all().order_by(
            "-date"
        )
        return context

    def form_valid(self, form):
        """
        Handle the form validation
        """
        context = self.get_context_data()
        user_form = context["user_form"]
        profile_form = context["profile_form"]
        with transaction.atomic():
            if user_form.is_valid() and profile_form.is_valid():
                user_form.instance = self.request.user
                profile_form.instance = self.object
                user_form.save()
                profile_form.save()
        return super(UpdateProfile, self).form_valid(form)

    def get_success_url(self):
        """
        Go to profile page after successful form submission
        """
        return reverse_lazy("profile")

    def form_invalid(self, form):
        """
        Show toast error message if the form is invalid
        """
        messages.error(
            self.request,
            "Oops, something went wrong! Please double-check the form.",
        )
        return super().form_invalid(form)


@login_required
@require_safe
def order_history(request, order_number):
    """
    Display order details from the profile page
    """
    order = get_object_or_404(OrderDetail, order_number=order_number)

    trunc_order_number = Truncator(order_number).chars(10, truncate="...")

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "from_profile": True,
        "trunc_order_number": trunc_order_number,
    }

    return render(request, template, context)
