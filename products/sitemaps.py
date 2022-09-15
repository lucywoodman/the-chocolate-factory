from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class ProductStaticSitemap(Sitemap):
    priority = 0.8
    protocol = "https"

    def items(self):
        return [
            "products",
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.64
    protocol = "https"

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return "/products/%s" % (obj.slug)
