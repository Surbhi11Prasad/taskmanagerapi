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
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()

    # Normal authenticated behavior
        if not self.request.user.is_authenticated:
            return Task.objects.none()

        return Task.objects.filter(
            owner=self.request.user,
            is_deleted=False
        )


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()