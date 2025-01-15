from django.urls import path
# from .views import LoginView, LogoutView, RegisterView

app_name = 'accounts'


# urlpatterns = [
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('register/', RegisterView.as_view(), name='register'),
# ]
from .views import CustomLogoutView, RegisterView, CustomLoginView
# from .views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]