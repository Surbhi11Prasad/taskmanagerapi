from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "get_assignee",
        "status",
        "priority",
        "is_deleted",
        "created_at",
    )

    list_filter = ("status", "priority", "is_deleted")
    search_fields = ("title", "description")

    def get_assignee(self, obj):
        return obj.assignee.username if obj.assignee else "-"
    
    get_assignee.short_description = "Assignee"
