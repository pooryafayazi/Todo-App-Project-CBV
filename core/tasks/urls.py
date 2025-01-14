from django.urls import path
from .views import TaskListView
# from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    # path('task/new/', TaskCreateView.as_view(), name='task_create'),
    # path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    # path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
