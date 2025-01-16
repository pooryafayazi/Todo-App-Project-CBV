from django.urls import path
# from .views import api_task_list_view
from .views import TaskList,TaskDetail
app_name = 'api-v1'

urlpatterns = [
    # path('task/', api_task_list_view,name='api-task-list'),
    # path('task/', TaskList, name='task-list'),
    path('task/', TaskList.as_view(), name='task-list'),
    # path('task/<int:id>/', taskDetail, name='task-detail'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),


]