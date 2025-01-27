from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.views import View
from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .models import User
from .forms import RegistrationForm, LoginForm


class CustomLogoutView(LogoutView):
    next_page = "accounts:login"


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User created: {user.email}, Active: {user.is_active}")
            login(request, user)
            return redirect("/")
        return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            login(request, user)
            return redirect("tasks:list_view")

        return render(request, "accounts/login.html", {"form": form})



# from django.http import HttpResponse
# import time
# from .tasks import sendEmail

# def send_email(response):
#     sendEmail.delay()
#     return HttpResponse("<h1>Done Sending after 3 sec witg sendEmail function<h1>")


# def test_postman(request):
#     response = requests.get('https://956f3b6d-2b9f-46dc-b079-42c81416fc1c.mock.pstmn.io/test/delay/5')
#     print(response.__dict__)
#     return JsonResponse(response.json())


# def test_postman(request):
#     if cache.get('test_delay_api') is None:
#         response = requests.get('https://956f3b6d-2b9f-46dc-b079-42c81416fc1c.mock.pstmn.io/test/delay/5')
#         # cache.set('test_delay_api', response.json(), timeout=60) # default timeout is 300 seconds
#         cache.set('test_delay_api', response.json())
#     return JsonResponse(cache.get('test_delay_api'))

@cache_page(60)
def test_postman(request):    
    response = requests.get('https://956f3b6d-2b9f-46dc-b079-42c81416fc1c.mock.pstmn.io/test/delay/5')
    return JsonResponse(response.json())