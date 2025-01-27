from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeatherView.as_view(), name='weather'),
]
