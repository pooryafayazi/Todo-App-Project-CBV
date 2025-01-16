from django.urls import path
# from .views import api_task_list_view
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('task', views.TaskViewSet, basename='task')


app_name = 'api-v1'

urlpatterns = [
    # path('task/', views.api_task_list_view,name='api-task-list'),
    # path('task/', views.TaskList, name='task-list'),
    # path('task/', views.TaskList.as_view(), name='task-list'),
    # path('task/<int:id>/', views.taskDetail, name='task-detail'),
    # path('task/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    # path('task/', views.TaskViewSet.as_view({'get':'list','post':'create'}), name='task-list'),
    # path('task/<int:pk>/', views.TaskViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}), name='task-list'),
]

urlpatterns += router.urls