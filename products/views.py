from django.shortcuts import get_object_or_404, render
from .models import Product


def full_range_products(request):
    """A view to return the full range of products, including sort/search queries"""

    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to return single product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)
