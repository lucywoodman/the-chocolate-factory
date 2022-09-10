from django.urls import path
from . import views

urlpatterns = [
    path("", views.Producers.as_view(), name="producers"),
    path("add/", views.AddProducer.as_view(), name="add_producer"),
    path(
        "update/<int:pk>",
        views.UpdateProducer.as_view(),
        name="update_producer",
    ),
    path(
        "delete/<int:pk>",
        views.DeleteProducer.as_view(),
        name="delete_producer",
    ),
]
