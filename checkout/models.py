from django.db import models
from products.models import Product
import uuid
from django.db.models import Sum
from django.conf import settings
from django.db.models.signals import pre_save


class OrderDetail(models.Model):
    class Meta:
        verbose_name = "Order"

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=256, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
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
    original_bag = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=256, null=False, blank=False, default=""
    )

    def _generate_order_number(self):
        """Creates a unique, random order number for the order"""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Calculates the grand total"""
        self.order_total = (
            self.orderitems.aggregate(Sum("item_total"))["item_total__sum"]
            or 0
        )
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


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

    def save(self, *args, **kwargs):
        """
        Override the save method to set the item total
        and update the order total.
        """
        self.item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SKU {self.product.sku} on order {self.order.order_number}"
