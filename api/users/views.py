from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.admin.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

    def list(self, request):
        return Response(
            {"detail": f'Method "{self.request.method}" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def create(self, request):
        return Response(
            {"detail": f'Method "{self.request.method}" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def update(self, request):
        return Response(
            {"detail": f'Method "{self.request.method}" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request):
        return Response(
            {"detail": f'Method "{self.request.method}" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request):
        return Response(
            {"detail": f'Method "{self.request.method}" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
