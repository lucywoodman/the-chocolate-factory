from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
    require_POST,
    require_GET,
)
from django.contrib import messages
from products.models import Product


@require_safe
def view_bag(request):
    """A view to return the bag contents page"""
    return render(request, "bag/bag.html")


@require_POST
def add_to_bag(request, item_id):
    """Add a qty of a specific item to the bag"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get("bag", {})

    if quantity > 99:
        messages.error(
            request,
            f"You cannot have more than 99 { product.name }'s in your bag.",
        )
    elif quantity < 0:
        messages.error(
            request,
            "You cannot add negative quantities. Please try again.",
        )
    elif item_id in list(bag.keys()):
        if bag[item_id] + quantity > 99:
            messages.error(
                request,
                f"You cannot have more than 99 { product.name }'s in your bag",
            )
        elif bag[item_id] + quantity < 0:
            messages.error(
                request,
                "You cannot add negative quantities. Please try again.",
            )
        else:
            bag[item_id] += quantity
            messages.success(
                request,
                f"You now have { bag[item_id] } \
                    x { product.name } in your bag.",
            )
    else:
        bag[item_id] = quantity
        messages.success(request, f"Added { product.name } to your bag.")

    request.session["bag"] = bag
    return redirect(redirect_url)


@require_POST
def adjust_bag(request, item_id):
    """Adjust the qty of a specific item in the bag"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))
    bag = request.session.get("bag", {})

    if quantity > 99:
        messages.error(
            request,
            f"You cannot have more than 99 { product.name }'s in your bag",
        )
    elif quantity > 0:
        if bag[item_id] + quantity > 99:
            messages.error(
                request,
                f"You cannot have more than 99 { product.name }'s in your bag",
            )
        elif bag[item_id] + quantity < 0:
            messages.error(
                request,
                "You cannot add negative quantities. Please try again.",
            )
        else:
            bag[item_id] = quantity
            messages.success(
                request,
                f"You now have { bag[item_id] } \
                    x { product.name } in your bag.",
            )
    else:
        bag.pop(item_id)
        messages.success(request, f"Removed { product.name } from your bag.")

    request.session["bag"] = bag
    return redirect(reverse("view_bag"))


@require_POST
def remove_from_bag(request, item_id):
    """Remove a specific item from the bag"""

    product = get_object_or_404(Product, pk=item_id)

    try:
        bag = request.session.get("bag", {})
        bag.pop(item_id)
        messages.success(request, f"Removed { product.name } from your bag.")

        request.session["bag"] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
