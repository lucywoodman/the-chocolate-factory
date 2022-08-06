from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib import messages
from django.db.models import Q
from .models import Product


def full_range_products(request):
    """A view to return the full range of products, including sort/search queries"""

    products = Product.objects.all()
    query = None

    if request.GET:
        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria."
                )
                return redirect(reverse("products"))

            queries = Q(name__icontains=query) | Q(details__icontains=query)
            products = products.filter(queries)

    context = {
        "products": products,
        "search_term": query,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to return single product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)
