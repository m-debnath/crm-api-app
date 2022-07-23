from core.logging.utils import log_performance_to_kafka
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    @log_performance_to_kafka
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["name"] = user.get_full_name()
        token["last_login"] = user.last_login.isoformat()

        return token
