from django.contrib import messages
from django.db.models import Q
from .models import Product
from django.views import generic


class FullProductRange(generic.ListView):
    """A view to return the full range of products, including sort/search queries"""

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

        if "category" in self.request.GET:
            category = self.request.GET.get("category")
            context["products"] = Product.objects.filter(
                category__slug=category
            )

        if "flavour" in self.request.GET:
            flavour = self.request.GET.get("flavour")
            context["products"] = Product.objects.filter(flavour__slug=flavour)

        return context


class ProductDetail(generic.DetailView):
    """Class for the product details view"""

    model = Product
    context_object_name = "product"
