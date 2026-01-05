# tasks/views.py
from rest_framework import generics, viewsets, permissions
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .serializers import UserRegisterSerializer, TaskSerializer
from .permissions import IsAdminOrManager



class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        if self.action in ["create", "update", "partial_update"]:
            return [IsAdminOrManager()]
        if self.action == "destroy":
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="admin").exists():
            return Task.objects.filter(is_deleted=False)

        if user.groups.filter(name="manager").exists():
            return Task.objects.filter(is_deleted=False)

        return Task.objects.filter(
            owner=user,
            is_deleted=False
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()