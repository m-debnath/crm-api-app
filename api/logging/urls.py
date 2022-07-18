from django.urls import path

from .views import log_to_kafka

urlpatterns = [
    path("", log_to_kafka),
]
