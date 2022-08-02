from django.shortcuts import render
from .models import Product


def full_range_products(request):
    """A view to return the full range of products, including sort/search queries"""

    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(request, "products/products.html", context)
