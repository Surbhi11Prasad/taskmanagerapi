from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Task

User = get_user_model()


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # ✅ JWT-style authentication for tests
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        response = self.client.post("/api/tasks/", {
            "title": "Test Task",
            "description": "Test description",
            "priority": 2
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_soft_delete(self):
        task = Task.objects.create(title="Task", owner=self.user)

        response = self.client.delete(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        task.refresh_from_db()
        self.assertTrue(task.is_deleted)
