from django.urls import path,include

from .views import CustomLogoutView, RegisterView, CustomLoginView

app_name = 'accounts'

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/v1/',include('accounts.api.v1.urls'))
    
]