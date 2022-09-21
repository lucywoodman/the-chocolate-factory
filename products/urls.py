from django.urls import path
from . import views

urlpatterns = [
    path("", views.FullProductRange.as_view(), name="products"),
    path("add/", views.add_product, name="add_product"),
    path(
        "update/<int:product_id>", views.update_product, name="update_product"
    ),
    path(
        "delete/<int:product_id>", views.delete_product, name="delete_product"
    ),
    path("<slug:slug>/", views.ProductDetail.as_view(), name="product_detail"),
]
