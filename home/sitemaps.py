from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeStaticSitemap(Sitemap):
    """
    Class to generate sitemap links
    """

    priority = 1.0
    protocol = "https"

    def items(self):
        return [
            "home",
            "privacy",
            "terms",
        ]

    def location(self, item):
        return reverse(item)
