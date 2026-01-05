from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="admin").exists()


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="manager").exists()


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=["admin", "manager"]).exists()
