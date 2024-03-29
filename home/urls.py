from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("privacy-policy/", views.privacy, name="privacy"),
    path("terms-and-conditions/", views.terms, name="terms"),
]
