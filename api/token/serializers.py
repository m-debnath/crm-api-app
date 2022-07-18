from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.logging.utils import log_memory_usage


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    @log_memory_usage
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username

        return token
