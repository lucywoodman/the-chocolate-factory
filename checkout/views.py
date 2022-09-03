from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from checkout.forms import OrderDetailForm


def checkout(request):
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "Looks like your bag is empty.")
        return redirect(reverse("products"))

    order_form = OrderDetailForm()
    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": "pk_test_51Ldu0HKBU8ZUeCZoApVNEozeMVRQVpC08w1YJaGj5w9Sd5jXzO0vpREnpV9OqWQMrh3aVqnuotuvNwh9dvIyxmlQ00YFkZ4gcB",
        "client_secret": "test",
    }

    return render(request, template, context)
