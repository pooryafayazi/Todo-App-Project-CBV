from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'complete', 'active', 'created_date', 'due_date', 'updated_date']
    search_fields = ['user', 'title', 'complete', 'active', 'created_date', 'due_date', 'updated_date']
    list_filter = ['user', 'title', 'complete', 'active', 'created_date', 'due_date', 'updated_date']
    
admin.site.register(Task, TaskAdmin)