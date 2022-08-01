from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

TYPE = (
    (0, "milk"),
    (1, "white"),
    (2, "dark"),
    (3, "black"),
    (4, "mixed"),
    (5, "alternative"),
)


class Category(models.Model):
    """Class for the category model"""

    name = models.CharField(max_length=256)
    nice_name = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_nice_name(self):
        """Returns nice_name"""
        return self.nice_name


class Product(models.Model):
    """Class for the product model"""

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    # producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    sku = models.CharField(max_length=10)
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    details = models.TextField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    ingredients = models.CharField(max_length=512, blank=True, null=True)
    # allergy_info = models.ForeignKey(Allergy, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.IntegerField(choices=TYPE, default=0)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


def slug_pre_save(instance, *args, **kwargs):
    """Saves the name as a slug before saving the instance object"""
    if instance.slug is None:
        instance.slug = slugify(instance.name)


pre_save.connect(slug_pre_save, sender=Product)
