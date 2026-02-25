from django.contrib import admin
from core.models import Task, Tag, TaskTag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at"]


class TaskTagInline(admin.TabularInline):
    """Inline para editar TaskTags dentro de Task"""

    model = TaskTag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "due_date", "created_at"]
    list_filter = ["status", "priority", "created_at"]
    search_fields = ["title", "description"]
    inlines = [TaskTagInline]
