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
    }

    return render(request, template, context)
