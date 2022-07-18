from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.logging.utils import log_performance_to_kafka


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    @log_performance_to_kafka
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username

        return token
