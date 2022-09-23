from django.db import models


class Producer(models.Model):
    """
    Class for the producer model
    """

    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    photo_url = models.URLField(max_length=1024, blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name
