from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Task


class UserRegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=["admin", "manager", "user"],
        default="user",
        write_only=True
    )

    class Meta:
        model = User
        fields = ("username", "password", "role")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role")
        user = User.objects.create_user(**validated_data)

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("owner", "is_deleted")
