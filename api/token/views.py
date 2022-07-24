from core.logging.utils import log_performance_to_kafka
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)


class MyTokenObtainPairVIew(TokenObtainPairView):
    @log_performance_to_kafka
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "refresh" in response.data.keys():
            response.set_cookie(
                "refresh",
                response.data["refresh"],
                httponly=True,
            )
            del response.data["refresh"]
        return response


class MyTokenRefreshView(TokenRefreshView):
    @log_performance_to_kafka
    def post(self, request, *args, **kwargs):
        if "refresh" not in request.data:
            request.data["refresh"] = request.COOKIES.get("refresh", "")
        response = super().post(request, *args, **kwargs)
        if "refresh" in response.data.keys():
            response.set_cookie(
                "refresh",
                response.data["refresh"],
                httponly=True,
            )
            del response.data["refresh"]
        return response


class MyTokenBlacklistView(TokenBlacklistView):
    @log_performance_to_kafka
    def post(self, request, *args, **kwargs):
        if "refresh" not in request.data:
            request.data["refresh"] = request.COOKIES.get("refresh", "")
        response = super().post(request, *args, **kwargs)
        return response
