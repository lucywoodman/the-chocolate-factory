from django.urls import path
from .views import SubscriptionView

app_name = "marketing"

urlpatterns = [
    path("", SubscriptionView.as_view(), name="subscription"),
]
