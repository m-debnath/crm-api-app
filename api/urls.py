from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import routers

from .views import MyTokenObtainPairView, getRoutes
from .users.views import UserViewSet

user_router = routers.DefaultRouter()
user_router.register("", UserViewSet)

urlpatterns = [
    path("", getRoutes),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("admin/", include("api.admin.urls")),
    path("users/", include(user_router.urls)),
]
