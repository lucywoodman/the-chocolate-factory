from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from producers.models import Producer


class Type(models.Model):
    """
    Class for the type model
    """

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Class for the category model
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Flavour(models.Model):
    """
    Class for the flavour model
    """

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Allergy(models.Model):
    """
    Class for the allergy model
    """

    class Meta:
        verbose_name_plural = "Allergies"

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Class for the product model
    """

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    flavour = models.ForeignKey(
        Flavour, on_delete=models.SET_NULL, blank=True, null=True
    )
    allergy_info = models.ManyToManyField(Allergy, blank=True)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    details = models.TextField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True, default="100")
    ingredients = models.CharField(max_length=512, blank=True, null=True)
    type = models.ManyToManyField(Type, blank=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override save method to generate a unique slug
        Using the slufify'd name + the product's pk
        """
        super(Product, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = f"{slugify(self.name)}-{self.id}"
            self.save()


def slug_pre_save(instance, *args, **kwargs):
    """
    Pre save function to generate slugs for smaller models
    """
    if not instance.slug:
        instance.slug = f"{slugify(instance.name)}"


pre_save.connect(slug_pre_save, sender=Category)
pre_save.connect(slug_pre_save, sender=Flavour)
pre_save.connect(slug_pre_save, sender=Allergy)
