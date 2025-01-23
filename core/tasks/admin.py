from django.contrib import admin
from .models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "creator",
        "title",
        "complete",
        "active",
        "created_date",
        "due_date",
        "updated_date",
    ]
    search_fields = [
        "creator",
        "title",
        "complete",
        "active",
        "created_date",
        "due_date",
        "updated_date",
    ]
    list_filter = [
        "creator",
        "title",
        "complete",
        "active",
        "created_date",
        "due_date",
        "updated_date",
    ]


admin.site.register(Task, TaskAdmin)
