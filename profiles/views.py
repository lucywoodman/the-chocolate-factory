from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from checkout.models import OrderDetail


@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(
                request,
                "Oops, something went wrong! Please double check the form.",
            )
    else:
        form = ProfileForm(instance=profile)

    orders = profile.orders.all()
    template = "profiles/profile.html"
    context = {
        "profile": profile,
        "form": form,
        "orders": orders,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(OrderDetail, order_number=order_number)

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "from_profile": True,
    }

    return render(request, template, context)
