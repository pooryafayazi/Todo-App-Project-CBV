from django.urls import path
# from .views import api_task_list_view
from .views import TaskList,TaskDetail
app_name = 'api-v1'

urlpatterns = [
    # path('task/', api_task_list_view,name='api-task-list'),
    path('task/', TaskList, name='task-list'),
    path('task/<int:id>/', TaskDetail, name='task-detail'),


]