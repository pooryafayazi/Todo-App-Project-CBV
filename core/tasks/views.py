from django.shortcuts import redirect
# from django.views.generic.list import ListView
# from django.views.generic.edit import (CreateView,UpdateView,DeleteView,)
# from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
# from .forms import TaskUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from .models import Task



from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

'''
class TaskListView(TemplateView):
    template_name = 'tasks/task_list3.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()        
        context['author'] = Task.objects.first().user
        return context
'''
    
'''    
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
'''

from django.views.generic import ListView
from .models import Task


class ActiveUserRequiredMixin(UserPassesTestMixin):
    def test_func(self, *args, **kwargs):
        return self.request.user.is_active

class TasksListView(ActiveUserRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list3.html'
    context_object_name = 'tasks'
    paginate_by = 6
    

    def get_queryset(self):
        
        # queryset = Task.objects.all()  
        context_object_name = 'tasks'
        
        queryset = Task.objects.filter(user=self.request.user)  
        
        filter_value = self.request.GET.get('filter')
        sort_value = self.request.GET.get('sort')
        # filter_value = self.request.GET.get('filter')
        # sort_value = self.request.GET.get('sort')
        if filter_value == '1':
             queryset = queryset.filter(title__isnull=False)
        elif filter_value == '2':
            queryset = queryset.filter(complete=True)
        elif filter_value == '3':
            queryset = queryset.filter(active=True)
        elif filter_value == '4':
            queryset = queryset.filter(due_date__isnull=False)


        if sort_value == '2':  
            queryset = queryset.order_by('due_date')
        else: 
            queryset = queryset.order_by('-created_date')

        return queryset
    
    
'''
class TaskDetailtView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
 '''   
    
    
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_list3.html'
    fields = ['title','due_date']
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_detail.html'
    fields = ['title','due_date']
    context_object_name = 'task'
    # form_class = TaskForm i didnt create TaskForm
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

'''    
class TaskCompleteView(UpdateView):
    model = Task
    template_name = 'tasks/task_list3.html'
    fields = ['title','due_date','complete']
    context_object_name = "tasks"
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
'''
class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.complete = not task.complete
        task.save()
        return redirect('tasks:list_view')
    
    
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = '/'

    
# class TaskCreateView(View):
#     def get(self, request):
#         form = TaskForm()
#         return render(request, 'tasks/task_form.html', {'form': form})

#     def post(self, request):
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#         return render(request, 'tasks/task_form.html', {'form': form})

# class TaskUpdateView(View):
#     def get(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         form = TaskForm(instance=task)
#         return render(request, 'tasks/task_form.html', {'form': form})

#     def post(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#         return render(request, 'tasks/task_form.html', {'form': form})

# class TaskDeleteView(View):
#     def post(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         task.delete()
#         return redirect('task_list')
