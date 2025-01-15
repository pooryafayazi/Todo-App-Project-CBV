from django.urls import path
from .views import TasksListView,TaskCreateView,TaskUpdateView,TaskDeleteView,TaskCompleteView

app_name = 'tasks'

urlpatterns = [
    path('', TasksListView.as_view(), name='list_view'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('edit/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='task-complete'),

]
