from django.urls import path
from .. import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    # registration
    path("registration/", views.RegistrationApiView.as_view(), name="registration"),
    # path('test-email', views.TestEmailSend.as_view(), name='test_email'),
    # activation
    path("activation/confirm/<str:token>",views.ActivationApiView.as_view(),name="activation",),
    # resend activation
    path("activation/resend/",views.ActivationResendApiView.as_view(),name="activation-resend",),
    # change pasword
    path("change-password/",views.ChangePasswordApiView.as_view(),name="change-password",),
    # reset password
    path("reset-password/", views.ResetPasswordApiView.as_view(), name="reset-password"),
    path("reset-password/confirm/<str:token>/",views.ResetPasswordConfirmApiView.as_view(), name="reset-password-confirm",),
    
    # login jwt
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    
    path('registrations/', views.RegistrationPageView.as_view(), name='registrations'),
    path('activations/', views.ActivationPageView.as_view(), name='activations'),
    path('change-passwords/', views.ChangePasswordPageView.as_view(), name='change-passwords'),
    path('reset-passwords/', views.ResetPasswordPageView.as_view(), name='reset-passwords'),
    path('reset-passwords/confirm/', views.ResetPasswordConfirmPageView.as_view(), name='reset-password-confirms'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    
    
    
    # login token
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
]
