from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.views import View
from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm,LoginForm 



class CustomLogoutView(LogoutView):
    next_page = 'accounts:login' 

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()  
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User created: {user.email}, Active: {user.is_active}")  
            login(request, user)  
            return redirect('/') 
        return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(View):
    def get(self, request):
        form = LoginForm()  
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            email = form.cleaned_data['email']
            user = User.objects.get(email=email) 
            login(request, user)  
            return redirect('tasks:list_view')  

        return render(request, 'accounts/login.html', {'form': form}) 
    
