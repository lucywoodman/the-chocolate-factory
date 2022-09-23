import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from producers.models import Producer
from ..models import Type, Category, Flavour, Allergy, Product


class TestProductViews(TestCase):
    """
    A class to test Product views
    """

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
        # create test products
        cls.product1 = Product.objects.create(
            category=cls.prod_category,
            flavour=cls.prod_flavour,
            producer=cls.producer,
            name="Test Product",
            price=9.99,
            weight=180,
            ingredients="test ingredients",
        )
        cls.product2 = Product.objects.create(
            category=cls.prod_category,
            flavour=cls.prod_flavour,
            producer=cls.producer,
            name="Test Product 2",
            price=9.99,
            weight=180,
            ingredients="test ingredients",
        )
        cls.product1.allergy_info.add(cls.prod_allergy)
        cls.product1.type.add(cls.prod_type)
        cls.product2.allergy_info.add(cls.prod_allergy)
        cls.product2.type.add(cls.prod_type)

        cls.password = str(uuid.uuid4())

        cls.superuser = User.objects.create_superuser(
            "testsuperuser", "testsuperuser@test.com", cls.password
        )
        cls.normuser = User.objects.create_user(
            "testnormuser", "testnormuser@test.com", cls.password
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    # Test products view
    def test_products_url_exists(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

    def test_products_view_accessible_by_name(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)

    def test_products_view_uses_correct_template(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    # Test product_detail view
    def test_product_detail_url_exists(self):
        response = self.client.get(f"/products/{self.product1.slug}/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_accessible_by_name(self):
        response = self.client.get(
            reverse("product_detail", kwargs={"slug": self.product1.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_uses_correct_template(self):
        response = self.client.get(
            reverse("product_detail", kwargs={"slug": self.product1.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")

    # Test add_product view
    def test_add_product_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("add_product"))
        self.assertRedirects(response, "/")

    def test_add_product_view_redirect_if_not_superuser(self):
        self.client.login(username="testnormuser", password=self.password)
        response = self.client.get(reverse("add_product"))
        self.assertRedirects(response, "/")

    def test_add_product_url_exists_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.get("/products/add/")
        self.assertEqual(str(response.context["user"]), "testsuperuser")
        self.assertEqual(response.status_code, 200)

    def test_add_product_view_accessible_by_name_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.get(reverse("add_product"))
        self.assertEqual(str(response.context["user"]), "testsuperuser")
        self.assertEqual(response.status_code, 200)

    def test_add_product_view_uses_correct_template_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.get(reverse("add_product"))
        self.assertEqual(str(response.context["user"]), "testsuperuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_form.html")

    # Test update_product view
    def test_update_product_view_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("update_product", kwargs={"pk": self.product1.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_update_product_view_redirect_if_not_superuser(self):
        self.client.login(username="testnormuser", password=self.password)
        response = self.client.get(
            reverse("update_product", kwargs={"pk": self.product1.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_update_product_url_exists_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.get(f"/products/update/{self.product1.id}")
        self.assertEqual(str(response.context["user"]), "testsuperuser")
        self.assertEqual(response.status_code, 200)

    def test_update_product_view_accessible_by_name_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.get(
            reverse("update_product", kwargs={"pk": self.product1.id})
        )
        self.assertEqual(str(response.context["user"]), "testsuperuser")
        self.assertEqual(response.status_code, 200)

    def test_update_product_view_uses_correct_template_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.get(
            reverse("update_product", kwargs={"pk": self.product1.id})
        )
        self.assertEqual(str(response.context["user"]), "testsuperuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_form.html")

    # Test delete_product view
    def test_delete_product_view_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("delete_product", kwargs={"pk": self.product1.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_delete_product_view_redirect_if_not_superuser(self):
        self.client.login(username="testnormuser", password=self.password)
        response = self.client.get(
            reverse("delete_product", kwargs={"pk": self.product1.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_delete_product_url_exists_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.post(f"/products/delete/{self.product1.id}")
        self.assertEqual(response.status_code, 302)

    def test_delete_product_view_accessible_by_name_if_superuser(self):
        self.client.login(username="testsuperuser", password=self.password)
        response = self.client.post(
            reverse("delete_product", kwargs={"pk": self.product2.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            "/products/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
