from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm
from django.views import generic


class FullProductRange(generic.ListView):
    """
    A view to return the full range of products,
    including sort/search queries
    """

    model = Product
    context_object_name = "products"
    template_name = "products/products.html"

    def get_ordering(self):
        ordering = self.request.GET.get("order_by")
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "q" in self.request.GET:
            query = self.request.GET.get("q")
            if not query:
                messages.error(
                    self.request, "You didn't enter any search criteria."
                )
            qs = Q(name__icontains=query) | Q(details__icontains=query)
            context["products"] = Product.objects.filter(qs)
            context["search_term"] = query

        if "category" in self.request.GET:
            category = self.request.GET.get("category")
            context["products"] = Product.objects.filter(
                category__slug=category
            )
            current_category = Category.objects.filter(slug=category)
            context["current_category"] = current_category

        if "flavour" in self.request.GET:
            flavour = self.request.GET.get("flavour")
            if flavour == "true":
                context["products"] = Product.objects.exclude(
                    flavour__isnull=True
                )
            else:
                context["products"] = Product.objects.filter(
                    flavour__slug=flavour
                )

        if "type" in self.request.GET:
            type = self.request.GET.get("type")
            if type == "vegan" and "category" in self.request.GET:
                category = self.request.GET.get("category")
                context["products"] = Product.objects.filter(
                    category__slug=category, type__name=type
                )
            else:
                context["products"] = Product.objects.filter(type__name=type)

        return context


class ProductDetail(generic.DetailView):
    """Class for the product details view"""

    model = Product
    context_object_name = "product"


@login_required
@require_http_methods(["GET", "POST"])
def add_product(request):
    if not request.user.is_superuser:
        messages.error(
            request, "You need proper authorisation to visit this page."
        )
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            return redirect(reverse("product_detail", args=[product.slug]))
        else:
            messages.error(
                request,
                "Oops, something went wrong! Please double-check the form.",
            )
    else:
        form = ProductForm()

    template = "products/add_product.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
@require_http_methods(["GET", "POST"])
def update_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(
            request, "You need proper authorisation to visit this page."
        )
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated product!")
            return redirect(reverse("product_detail", args=[product.slug]))
        else:
            messages.error(
                request,
                "Oops, something went wrong! Please double-check the form.",
            )
    else:
        form = ProductForm(instance=product)

    template = "products/update_product.html"
    context = {
        "form": form,
        "product": product,
    }

    return render(request, template, context)


@login_required
@require_http_methods(["GET", "POST"])
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(
            request, "You need proper authorisation to visit this page."
        )
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "Successfully deleted product!")
    return redirect(reverse("products"))
