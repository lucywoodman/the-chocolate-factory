from django.urls import path
from . import views

urlpatterns = [
    path("", views.Producers.as_view(), name="producers"),
    path("add/", views.AddProducer.as_view(), name="add_producer"),
]
