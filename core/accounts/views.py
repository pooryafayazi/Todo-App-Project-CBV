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
        
        
        
        