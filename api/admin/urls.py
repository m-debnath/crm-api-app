from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet


user_router = routers.DefaultRouter()
user_router.register("", UserViewSet)

urlpatterns = [
    path("users/", include(user_router.urls)),
]
