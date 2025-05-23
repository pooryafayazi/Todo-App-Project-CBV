from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.base import TemplateView
from django.http import JsonResponse
import json

from accounts.models import Profile
from .models import Task
from weather.views import WeatherView


"""
class TaskListView(TemplateView):
    template_name = 'tasks/task_list3.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['author'] = Task.objects.first().user
        return context
"""

"""
class TListView(ListView):
    # model = Task
    queryset = Task.objects.all()
    template_name = 'tasks/task_list3.html'
    context_object_name = 'tasks'
    paginate_by = 6
    
    def get_queryset(self):
        return Task.objects.all()
        # return Task.objects.filter(complete=Flase)
        # return Task.objects.filter(active=True)
"""


class ActiveUserRequiredMixin(UserPassesTestMixin):
    def test_func(self, *args, **kwargs):
        return self.request.user.is_active


class TasksListView(ActiveUserRequiredMixin, ListView):
# class TasksListView(ListView):
    model = Task
    template_name = "tasks/task_list3.html"
    context_object_name = "tasks"
    paginate_by = 6

    def get_queryset(self):
        # queryset = Task.objects.all()
        profile_instance = get_object_or_404(Profile, user=self.request.user)
        # queryset = Task.objects.filter(user=self.request.user)
        queryset = Task.objects.filter(creator=profile_instance)
        filter_value = self.request.GET.get("filter")
        sort_value = self.request.GET.get("sort")
        # filter_value = self.request.GET.get('filter')
        # sort_value = self.request.GET.get('sort')
        if filter_value == "1":
            queryset = queryset.filter(title__isnull=False)
        elif filter_value == "2":
            queryset = queryset.filter(complete=True)
        elif filter_value == "3":
            queryset = queryset.filter(active=True)
        elif filter_value == "4":
            queryset = queryset.filter(due_date__isnull=False)

        if sort_value == "2":
            queryset = queryset.order_by("due_date")
        else:
            queryset = queryset.order_by("-created_date")

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        

        request = self.request
        weather_view = WeatherView.as_view()
        response = weather_view(request)
        
        if isinstance(response, JsonResponse):
            # Decode the JSON response
            weather_data = response.content.decode('utf-8')
            # Parse it to a Python dict
            context['weather_data'] = json.loads(weather_data)
        else:
            context['weather_data'] = {'error': 'Unable to fetch weather data.'}

        return context
    
    
    
    
class TasksListApiView(ActiveUserRequiredMixin, TemplateView):
    template_name = 'tasks/task_list_api.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['tasks'] = Task.objects.all()
    #     return context


class TaskCreateView(LoginRequiredMixin, CreateView):
# class TaskCreateView( CreateView):
    model = Task
    template_name = "tasks/task_list3.html"
    fields = ["title", "due_date"]
    success_url = "/"

    def form_valid(self, form):
        profile_instance = get_object_or_404(Profile, user=self.request.user)
        form.instance.creator = profile_instance
        # form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
# class TaskUpdateView(UpdateView):
    model = Task
    template_name = "tasks/task_detail.html"
    fields = ["title", "due_date"]
    context_object_name = "task"
    # form_class = TaskForm i didnt create TaskForm
    success_url = "/"

    def form_valid(self, form):
        profile_instance = get_object_or_404(Profile, user=self.request.user)
        form.instance.creator = profile_instance
        # form.instance.user = self.request.user
        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, View):
# class TaskCompleteView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.complete = not task.complete
        task.active = not task.active
        task.save()
        return redirect("tasks:list_view")


class TaskDeleteView(DeleteView):
    model = Task
    context_object_name = "task"
    success_url = "/"

