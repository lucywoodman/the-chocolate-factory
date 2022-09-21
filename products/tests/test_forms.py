from django.test import TestCase
from ..forms import ProductForm


class TestProductForm(TestCase):
    """A class to test the Product form"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_form_fields_populate(self):
        form = ProductForm()
        self.assertIn("name", form.fields)
        self.assertIn("producer", form.fields)
        self.assertIn("price", form.fields)
        self.assertIn("weight", form.fields)
        self.assertIn("type", form.fields)
        self.assertIn("category", form.fields)
        self.assertIn("flavour", form.fields)
        self.assertIn("allergy_info", form.fields)
        self.assertIn("details", form.fields)
        self.assertIn("ingredients", form.fields)
        self.assertIn("image", form.fields)

    def test_form_hidden_fields_dont_populate(self):
        form = ProductForm()
        self.assertNotIn("slug", form.fields)

    def test_form_validation_for_empty_field(self):
        form = ProductForm(data={"name": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])
