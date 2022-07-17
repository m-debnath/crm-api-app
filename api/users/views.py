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

    def list(self, request):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        requesting_user = self.request.user
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if requesting_user.id != user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return Response(serializer.data)
