from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("api/v1/", include("accounts.api.v1.urls")),
    # path('send-email/', views.send_email, name='send-email'),
    path('test/', views.test_postman, name='test-postman'),

]
