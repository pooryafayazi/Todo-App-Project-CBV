from django.urls import path
from .views import TaskListView, TasksListView,TaskDetailtView,TaskCreateView,TaskUpdateView,TaskDeleteView,TaskCompleteView
from django.views.generic import RedirectView
# from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView

app_name = 'tasks'

urlpatterns = [
    # path('gotoitmeter', RedirectView.as_view(url='https://www.itmeter.ir/'), name='gotoitmeter'),
    # path('cbv-task', RedirectView.as_view(pattern_name='tasks:task_list' ), name='gotoitmeter'),
    
    # path('tasks', TaskListView.as_view(), name='task_list'),
    
    
    path('', TasksListView.as_view(), name='list_view'),
    # path('task/<int:pk>/', TaskDetailtView.as_view(), name='task-detail'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('edit/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='task-complete'),
        
    # path('task/new/', TaskCreateView.as_view(), name='task_create'),
    # path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    # path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
