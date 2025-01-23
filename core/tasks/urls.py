from django.urls import path, include
from . import views
    
app_name = "tasks"

urlpatterns = [
    path("", views.TasksListView.as_view(), name="list_view"),
    path("create/", views.TaskCreateView.as_view(), name="task-create"),
    path("edit/<int:pk>/", views.TaskUpdateView.as_view(), name="task-update"),
    path("delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("complete/<int:pk>/", views.TaskCompleteView.as_view(), name="task-complete"),
    path("api/v1/", include("tasks.api.v1.urls")),
    
    
    # test
    # path('', views.IndexView.as_view(), name='index'),
    
]
