from django.urls import path, include
from rest_framework import routers

from api.views import getRoutes
from api.users.views import UserViewSet

user_router = routers.DefaultRouter()
user_router.register("", UserViewSet)

urlpatterns = [
    path("", getRoutes),
    path("token/", include("api.token.urls")),
    path("admin/", include("api.admin.urls")),
    path("users/", include(user_router.urls)),
]
