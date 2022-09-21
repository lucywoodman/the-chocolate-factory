import re
from decimal import Decimal
from sqlite3 import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from producers.models import Producer
from products.models import Type, Category, Flavour, Allergy, Product
from ..models import OrderDetail, OrderItem


class TestOrderModel(TestCase):
    """A class to test the Order model"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create test producer
        cls.producer = Producer.objects.create(
            name="Test Producer",
            location="Test Location",
        )
        # create test product type
        cls.prod_type = Type.objects.create(name="test type")
        # create test product category
        cls.prod_category = Category.objects.create(name="test category")
        # create test product flavour
        cls.prod_flavour = Flavour.objects.create(name="test flavour")
        # create test product allergy
        cls.prod_allergy = Allergy.objects.create(name="test allergy")
        # create test product
        cls.product = Product.objects.create(
            category=cls.prod_category,
            flavour=cls.prod_flavour,
            producer=cls.producer,
            name="Test Product",
            price=9.99,
            weight=180,
            ingredients="test ingredients",
        )
        cls.product.allergy_info.add(cls.prod_allergy)
        cls.product.type.add(cls.prod_type)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_order_generate_order_number(self):
        # does order_number match regex for uuid4.hex
        order = OrderDetail()
        regex = re.compile("[0-9A-F]{32}\Z")
        self.assertRegex(order._generate_order_number(), regex)

    def test_order_update_total(self):
        # does order_total update after adding order items
        order = OrderDetail()
        order.save()
        self.assertEqual(order.order_total, 0)
        orderitem = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
        )
        self.assertEqual(
            order.order_total, Decimal("19.98").quantize(Decimal(".01"))
        )

    def test_order_delivery_cost(self):
        # does order delivery_cost = 10% of order_total
        order = OrderDetail()
        order.save()
        orderitem = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
        )
        self.assertEqual(
            order.delivery_cost,
            Decimal(order.order_total * Decimal("0.1")).quantize(
                Decimal(".01")
            ),
        )

    def test_order_free_delivery_when_threshold_met(self):
        # does delivery_cost = 0 when order over 30
        order = OrderDetail()
        order.save()
        orderitem = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=4,  # 4 * 9.99 = 39.96
        )
        self.assertEqual(
            order.order_total, Decimal("39.96").quantize(Decimal(".01"))
        )
        self.assertEqual(order.delivery_cost, Decimal("0"))

    def test_order_grand_total(self):
        # does grand_total = order_total + delivery_cost
        order = OrderDetail()
        order.save()
        orderitem = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
        )
        self.assertEqual(
            order.order_total + order.delivery_cost,
            Decimal(19.98 + (19.98 * 0.1)).quantize(Decimal(".01")),
        )


class TestOrderItemModel(TestCase):
    """A class to test the OrderItem model"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create test producer
        cls.producer = Producer.objects.create(
            name="Test Producer",
            location="Test Location",
        )
        # create test product type
        cls.prod_type = Type.objects.create(name="test type")
        # create test product category
        cls.prod_category = Category.objects.create(name="test category")
        # create test product flavour
        cls.prod_flavour = Flavour.objects.create(name="test flavour")
        # create test product allergy
        cls.prod_allergy = Allergy.objects.create(name="test allergy")
        # create test product
        cls.product = Product.objects.create(
            category=cls.prod_category,
            flavour=cls.prod_flavour,
            producer=cls.producer,
            name="Test Product",
            price=9.99,
            weight=180,
            ingredients="test ingredients",
        )
        cls.product.allergy_info.add(cls.prod_allergy)
        cls.product.type.add(cls.prod_type)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_orderitem_qty_min_set_to_1(self):
        order = OrderDetail()
        order.save()
        orderitem = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=-999999,
        )
        self.assertEqual(orderitem.quantity, 1)

    def test_orderitem_qty_max_set_to_99(self):
        order = OrderDetail()
        order.save()
        orderitem = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=999999,
        )
        self.assertEqual(orderitem.quantity, 99)
