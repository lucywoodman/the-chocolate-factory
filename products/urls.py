from django.urls import path
from . import views

urlpatterns = [
    path("", views.FullProductRange.as_view(), name="products"),
    path("add/", views.AddProduct.as_view(), name="add_product"),
    path(
        "update/<int:pk>",
        views.UpdateProduct.as_view(),
        name="update_product",
    ),
    path(
        "delete/<int:pk>", views.DeleteProduct.as_view(), name="delete_product"
    ),
    path("<slug:slug>/", views.ProductDetail.as_view(), name="product_detail"),
]
