from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

# from django.core.mail import send_mail
# from mail_templated import send_mail
from mail_templated import EmailMessage
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

# from datetime import datetime
import datetime
import pytz

from .serializers import (
    RegistrationSerializer,
    #CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from ..utils import EmailThread
from ...models import Profile
from ...models import UsedResetToken

# from ...models import User

User = get_user_model()
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer

class LoginApiView(generics.GenericAPIView, TemplateView):
    serializer_class = LoginSerializer
    template_name = 'accounts/login-api.html'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = self.get_tokens_for_user(user)
            return Response({'access': token, 'email': user.email}, status=200)

            # if user is not None:
            #     token = self.get_tokens_for_user(user)
            #     return redirect('tasks:api-v1:lists')

        return Response({'errors': serializer.errors}, status=400)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
class PasswordResetRequestView(generics.CreateAPIView, TemplateView):    
    serializer_class = PasswordResetRequestSerializer
    template_name = 'accounts/password_reset_request.html'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"detail": "Password reset code sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.UpdateAPIView, TemplateView):
    serializer_class = PasswordResetConfirmSerializer
    template_name = 'accounts/password_reset_confirmation.html'

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)


"""
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
"""


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    template_name = 'accounts/registration.html'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)

            # Send activation email
            email_obj = EmailMessage(
                subject="Account Activation",
                body=f"Activate your account using this token: {token}",
                from_email="admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            
            return redirect('login') 

        return render(request, self.template_name, {'errors': serializer.errors})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


  

"""
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})
"""


"""
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


 
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


"""
class TestEmailSend(generics.GenericAPIView):
       
    def get(self, request, *args, **kwargs):
        self.email = 'sarbaz@sarbaz.com'
        user_obj = get_object_or_404(User, email = self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'admin@admin.com', to=[self.email])
        EmailThread(email_obj).start()
        return Response('Email sent')
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
 """


class ActivationApiView(APIView):

    def get(self, request, token, *args, **kwargs):
        # decode > id user
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        # object user
        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_verified:
            return Response({"details": "Your account has already verified."})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "Your account has been verified and activated successfully."}
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "User activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.generate_reset_token(user_obj)
        email_obj = EmailMessage(
            "email/reset_password.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "Password reset email sent successfully"},
            status=status.HTTP_200_OK,
        )

    def generate_reset_token(self, user):
        local_tz = pytz.timezone("Asia/Tehran")
        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.now(local_tz) + datetime.timedelta(hours=12),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token


"""
class ResetPasswordConfirmApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': _('Password has been reset successfully.')}, status=status.HTTP_200_OK)
 """


class ResetPasswordConfirmApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            if UsedResetToken.objects.filter(token=token).exists():
                return Response(
                    {"detail": _("This token has already been used.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
            user = User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return Response(
                {"detail": _("Invalid or expired token.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        UsedResetToken.objects.create(token=token)

        return Response(
            {"detail": _("Password has been reset successfully.")},
            status=status.HTTP_200_OK,
        )



class RegistrationPageView(TemplateView):
    template_name = 'accounts/registration.html'

class ActivationPageView(TemplateView):
    template_name = 'accounts/activation.html'

class ChangePasswordPageView(TemplateView):
    template_name = 'accounts/change_password.html'

class ResetPasswordPageView(TemplateView):
    template_name = 'accounts/reset_password.html'

class ResetPasswordConfirmPageView(TemplateView):
    template_name = 'accounts/reset_password_confirm.html'

class LoginPageView(TemplateView):
    template_name = 'accounts/login.html'

# class LoginPageView(TemplateView):
#     template_name = 'accounts/login.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         return redirect('home')