from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import MyTokenBlacklistView, MyTokenObtainPairVIew, MyTokenRefreshView

urlpatterns = [
    path("", MyTokenObtainPairVIew.as_view(), name="token_obtain_pair"),
    path("refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("blacklist/", MyTokenBlacklistView.as_view(), name="token_blacklist"),
]
