from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from core.logging.utils import log_memory_usage


@api_view(["GET"])
@log_memory_usage
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
        "/api/token/verify",
        "/api/token/blacklist",
        "/api/admin/users",
        "/api/users",
    ]

    return Response(routes)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    @log_memory_usage
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
