from django.urls import path
# from .views import api_task_list_view
from .views import TaskDetail,TaskViewSet
app_name = 'api-v1'

urlpatterns = [
    # path('task/', api_task_list_view,name='api-task-list'),
    # path('task/', TaskList, name='task-list'),
    # path('task/', TaskList.as_view(), name='task-list'),
    # path('task/<int:id>/', taskDetail, name='task-detail'),
    # path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('task/', TaskViewSet.as_view({'get':'list','post':'create'}), name='task-list'),
    path('task/<int:pk>/', TaskViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}), name='task-list'),



]