from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ProducerStaticSitemap(Sitemap):
    """
    Class to generate sitemap links
    """

    priority = 0.8
    protocol = "https"

    def items(self):
        return [
            "producers",
        ]

    def location(self, item):
        return reverse(item)
