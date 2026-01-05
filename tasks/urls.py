# tasks/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserRegisterView

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
]

urlpatterns += router.urls
