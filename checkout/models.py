from decimal import Decimal
import uuid
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
from products.models import Product
from profiles.models import Profile


class OrderDetail(models.Model):
    class Meta:
        verbose_name = "Order"

    order_number = models.CharField(max_length=32, null=False, editable=False)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=256, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label="Country *", null=False, blank=False)
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
        order_total = (
            self.orderitems.aggregate(models.Sum("item_total"))[
                "item_total__sum"
            ]
            or 0
        )
        self.order_total = Decimal(order_total).quantize(Decimal(".01"))
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
            self.delivery_cost = Decimal(delivery_cost).quantize(
                Decimal(".01")
            )
        else:
            self.delivery_cost = 0
        grand_total = self.order_total + self.delivery_cost
        self.grand_total = Decimal(grand_total).quantize(Decimal(".01"))
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
    quantity = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    item_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__range=(1, 99)),
                name="quantity_range",
            ),
        ]

    def save(self, *args, **kwargs):
        """
        Override the save method to set the item total
        and update the order total.
        """
        if self.quantity < 1:
            self.quantity = 1
        if self.quantity > 99:
            self.quantity = 99
        total = self.product.price * self.quantity
        self.item_total = Decimal(total).quantize(Decimal(".01"))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} on order {self.order.order_number}"
