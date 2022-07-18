from django.urls import include, path
from rest_framework import routers

from api.users.views import UserViewSet
from api.views import getRoutes

user_router = routers.DefaultRouter()
user_router.register("", UserViewSet)

urlpatterns = [
    path("", getRoutes),
    path("token/", include("api.token.urls")),
    path("admin/", include("api.admin.urls")),
    path("logging/", include("api.logging.urls")),
    path("users/", include(user_router.urls)),
]
