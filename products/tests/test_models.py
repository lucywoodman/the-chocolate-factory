from django.test import TestCase
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from producers.models import Producer
from ..models import Type, Category, Flavour, Allergy, Product


class TestTypeModel(TestCase):
    """A class to test the Type model"""

    def test_type_name_char_limit(self):
        type = Type.objects.create(name="test type")
        with self.assertRaises(ValidationError):
            type.name = "A name longer than twenty five chars"
            type.full_clean()
            type.save()

    def test_type_has_string_method(self):
        type = Type.objects.create(name="test type")
        self.assertEqual(str(type), "test type")


class TestCategoryModel(TestCase):
    """A class to test the Category model"""

    def test_category_name_char_limit(self):
        with self.assertRaises(ValidationError):
            category = Category.objects.create(
                name="A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars"
            )
            category.full_clean()

    def test_category_has_slug(self):
        category = Category.objects.create(name="test category")
        self.assertEqual(category.slug, slugify(category.name))

    def test_category_has_string_method(self):
        category = Category.objects.create(name="test category")
        self.assertEqual(str(category), "test category")


class TestFlavourModel(TestCase):
    """A class to test the Flavour model"""

    def test_flavour_name_char_limit(self):
        with self.assertRaises(ValidationError):
            flavour = Flavour.objects.create(
                name="A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars \
                A name longer than two hundred and fifty six chars"
            )
            flavour.full_clean()

    def test_flavour_has_slug(self):
        flavour = Flavour.objects.create(name="test flavour")
        self.assertEqual(flavour.slug, slugify(flavour.name))

    def test_flavour_has_string_method(self):
        flavour = Flavour.objects.create(name="test flavour")
        self.assertEqual(str(flavour), "test flavour")


class TestAllergyModel(TestCase):
    """A class to test the Allergy model"""

    def test_allergy_name_char_limit(self):
        with self.assertRaises(ValidationError):
            allergy = Allergy.objects.create(
                name="A name longer than two hundred and fifty six chars \
                    A name longer than two hundred and fifty six chars \
                    A name longer than two hundred and fifty six chars \
                    A name longer than two hundred and fifty six chars \
                    A name longer than two hundred and fifty six chars \
                    A name longer than two hundred and fifty six chars"
            )
            allergy.full_clean()

    def test_allergy_has_slug(self):
        allergy = Allergy.objects.create(name="test allergy")
        self.assertEqual(allergy.slug, slugify(allergy.name))

    def test_allergy_has_string_method(self):
        allergy = Allergy.objects.create(name="test allergy")
        self.assertEqual(str(allergy), "test allergy")


class TestProductModel(TestCase):
    """A class to test the Product model"""

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

    def test_product_has_slug(self):
        product = self.product
        self.assertEqual(product.slug, slugify(product.name))

    def test_product_has_string_method(self):
        product = self.product
        self.assertEqual(str(product), "Test Product")
