
'''

from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from .forms import UserRegistrationForm

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks:list_view')
        return render(request, 'accounts/login.html', {'form': form})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
'''


from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import LogoutView
from django.views import View
from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm,LoginForm  # You’ll need to create this form

# class CustomLoginView(LoginView):
    # template_name = 'accounts/login.html'  # Your login template here

class CustomLogoutView(LogoutView):
    next_page = 'accounts:login'  # Redirect to login page after logout

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()  # Initialize your registration form
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User created: {user.email}, Active: {user.is_active}")  # Debugging line
            login(request, user)  # Log the user in after registration
            return redirect('/')  # Redirect to a home page or dashboard
        return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(View):
    def get(self, request):
        form = LoginForm()  # Initialize the form
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)  # Create the form with POST data
        if form.is_valid():  # Check if the form is valid
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)  # Get the user instance directly
            login(request, user)  # Log the user in
            return redirect('tasks:list_view')  # Redirect to the task list view

        return render(request, 'accounts/login.html', {'form': form})  # Re-render the form with errors
    
    
    



'''
class LoginView(View):
    def get(self, request):
        form = LoginForm()  # Initialize your login form
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # احراز هویت کاربر با استفاده از ایمیل
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('/')  # Redirect to a home page or dashboard
            else:
                form.add_error(None, "Invalid email or password.")
        
        return render(request, 'accounts/login.html', {'form': form})
'''



'''
class CustomLoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('tasks:list_view')
            else:
                return render(request, 'accounts/login.html', {'error': 'This account is inactive.'})
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials.'})
'''     
        
        
        
'''
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks:list_view")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks:list_view")
        return super(RegisterView, self).get(*args, **kwargs)
'''        
        
        
        
        