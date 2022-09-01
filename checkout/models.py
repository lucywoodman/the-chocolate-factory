from django.db import models
from products.models import Product
import uuid
from django.db.models import Sum
from django.conf import settings
from django.db.models.signals import pre_save


class OrderDetail(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=256, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )

    def __str__(self):
        return self.order_number


def order_number_pre_save(instance, *args, **kwargs):
    """Saves a unique order number to the order before saving the instance object"""
    if instance.order_number is None:
        instance.order_number = uuid.uuid4().hex.upper()


def update_total_pre_save(instance, *args, **kwargs):
    """Calculates the grand_total"""
    instance.order_total = instance.orderitems.aggregate(Sum("item_total"))[
        "item_total__sum"
    ]
    if instance.order_total < settings.FREE_DELIVERY_THRESHOLD:
        instance.delivery_cost = (
            instance.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        )
    else:
        instance.delivery_cost = 0
    instance.grand_total = instance.order_total + instance.delivery_cost
    instance.save()


pre_save.connect(order_number_pre_save, sender=OrderDetail)
pre_save.connect(update_total_pre_save, sender=OrderDetail)


class OrderItem(models.Model):
    order = models.ForeignKey(
        OrderDetail,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="orderitems",
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.SmallIntegerField(null=False, blank=False, default=0)
    item_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def __str__(self):
        return f"SKU {self.product.sku} on order {self.order.order_number}"
