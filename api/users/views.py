from api.admin.serializers import UserSerializer
from api.utils import method_not_allowed_message
from core.logging.utils import log_performance_to_kafka
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @log_performance_to_kafka
    def retrieve(self, request, pk=None):
        requesting_user = self.request.user
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if requesting_user.id != user.id:
            return Response(
                {"detail": "You can only request details of your own user."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def list(self, _):
        return Response(
            method_not_allowed_message(self.request.method),
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def create(self, _):
        return Response(
            method_not_allowed_message(self.request.method),
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def update(self, _):
        return Response(
            method_not_allowed_message(self.request.method),
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, _):
        return Response(
            method_not_allowed_message(self.request.method),
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, _):
        return Response(
            method_not_allowed_message(self.request.method),
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
