from django.test import TestCase
from django.db import IntegrityError
from producers.models import Producer
from ..models import Type, Category, Flavour, Allergy, Product


class TestProductForm(TestCase):
    """A class to test the Product form"""

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

    def test_slug_is_unique(self):
        product1 = self.product
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                producer=product1.producer,
                name="Test Product",
                price=9.99,
                weight=180,
            )
