import json

import stripe
from bag.contexts import bag_contents
from django.conf import settings
from django.contrib import messages
from django.shortcuts import (
    HttpResponse,
    get_object_or_404,
    redirect,
    render,
    reverse,
)
from django.utils.text import Truncator
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)
from products.models import Product
from profiles.forms import ProfileForm
from profiles.models import Profile

from .forms import OrderDetailForm
from .models import OrderDetail, OrderItem


@require_POST
def cache_checkout_data(request):
    """
    Function to capture checkout data
    """
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(request.session.get("bag", {})),
                "save_info": request.POST.get("save_info"),
                "username": request.user,
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            (
                "Sorry, your payment cannot be "
                "processed right now. Please try "
                "again later."
            ),
        )
        return HttpResponse(content=e, status=400)


@require_http_methods(["GET", "POST"])
def checkout(request):
    """
    Function to handle the checkout page/form
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        bag = request.session.get("bag", {})

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "town_or_city": request.POST["town_or_city"],
            "county": request.POST["county"],
            "postcode": request.POST["postcode"],
            "country": request.POST["country"],
        }
        order_form = OrderDetailForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps("bag")
            order.save()
            for item_id, quantity in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "Oops, looks like an item is missing from our database! \
                            Please contact us for assistance.",
                    )
                    order.delete()
                    return redirect(reverse("view_bag"))

            request.session["save_info"] = "save-info" in request.POST
            return redirect(
                reverse("checkout_success", args=[order.order_number])
            )
        else:
            messages.error(
                request, "There's a problem with the form. Please try again."
            )
    else:
        bag = request.session.get("bag", {})
        if not bag:
            messages.error(request, "Looks like your bag is empty.")
            return redirect(reverse("products"))

        current_bag = bag_contents(request)
        total = current_bag["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                order_form = OrderDetailForm(
                    initial={
                        "full_name": profile.user.get_full_name(),
                        "email": profile.user.email,
                        "phone_number": profile.default_phone_number,
                        "street_address1": profile.default_street_address1,
                        "street_address2": profile.default_street_address2,
                        "town_or_city": profile.default_town_or_city,
                        "county": profile.default_county,
                        "postcode": profile.default_postcode,
                        "country": profile.default_country,
                    }
                )
            except Profile.DoesNotExist:
                order_form = OrderDetailForm()
        else:
            order_form = OrderDetailForm()

    if not stripe_public_key:
        messages.warning(request, "Stripe public key is missing.")

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, template, context)


@require_safe
def checkout_success(request, order_number):
    """
    Function for successful checkout
    """
    save_info = request.session.get("save_info")
    order = get_object_or_404(OrderDetail, order_number=order_number)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        order.profile = profile
        order.save()

        if save_info:
            profile_data = {
                "default_phone_number": order.phone_number,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_town_or_city": order.town_or_city,
                "default_county": order.county,
                "default_postcode": order.postcode,
                "default_country": order.country,
            }
            profile_form = ProfileForm(profile_data, instance=profile)
            if profile_form.is_valid():
                profile_form.save()

    trunc_order_number = Truncator(order_number).chars(10, truncate="...")

    messages.success(
        request,
        f"Order successfully processed! \
        A confirmation email will be sent to {order.email}.",
    )

    if "bag" in request.session:
        del request.session["bag"]

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "trunc_order_number": trunc_order_number,
    }

    return render(request, template, context)
