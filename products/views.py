from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Flavour


def full_range_products(request):
    """A view to return the full range of products, including sort/search queries"""

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if "category" in request.GET:
            categories = request.GET["category"]
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if "flavour" in request.GET:
            flavours = request.GET["flavour"]
            products = products.filter(flavour__name__in=flavours)
            flavours = Flavour.objects.filter(name__in=flavours)

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
        "current_categories": categories,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to return single product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)
