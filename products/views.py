from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
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


class AddProduct(UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
    """
    A view to display the product form.
    To add new products. Restricted to superusers only.
    """

    model = Product
    form_class = ProductForm
    success_message = "Successfully added product!"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")

    def get_success_url(self):
        return reverse("product_detail", args=[self.object.slug])

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Oops, something went wrong! Please double-check the form.",
        )
        return super().form_invalid(form)


class UpdateProduct(
    UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView
):
    """
    A view to display the product form.
    To update products. Restricted to superusers only.
    """

    model = Product
    form_class = ProductForm
    success_message = "Successfully updated product!"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")

    def get_success_url(self):
        return reverse("product_detail", args=[self.object.slug])

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Oops, something went wrong! Please double-check the form.",
        )
        return super().form_invalid(form)


class DeleteProduct(
    UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView
):
    """
    A view to delete products.
    Restricted to superusers only.
    """

    model = Product
    template = "products/products.html"
    success_message = "Successfully deleted product!"
    success_url = reverse_lazy("products")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request, "You need proper authorisation to do that."
        )
        return redirect("home")
