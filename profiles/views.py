from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.text import Truncator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_safe
from .models import Profile
from .forms import ProfileForm, UserForm
from checkout.models import OrderDetail


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(
                request,
                "Oops, something went wrong! Please double check the form.",
            )
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    orders = profile.orders.all().order_by("-date")
    template = "profiles/profile.html"
    context = {
        "profile": profile,
        "user_form": user_form,
        "profile_form": profile_form,
        "orders": orders,
    }

    return render(request, template, context)


@login_required
@require_safe
def order_history(request, order_number):
    order = get_object_or_404(OrderDetail, order_number=order_number)

    trunc_order_number = Truncator(order_number).chars(10, truncate="...")

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "from_profile": True,
        "trunc_order_number": trunc_order_number,
    }

    return render(request, template, context)
