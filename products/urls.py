from django.urls import path
from . import views

urlpatterns = [
    path("", views.FullProductRange.as_view(), name="products"),
    path("<slug:slug>", views.ProductDetail.as_view(), name="product_detail"),
]
