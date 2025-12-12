from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    assignee = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "owner", "assignee",
            "status", "priority", "due_date", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]
