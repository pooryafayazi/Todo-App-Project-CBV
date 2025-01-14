from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,UpdateView,DeleteView,)
from django.urls import reverse_lazy
from .forms import TaskUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Task



from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'tasks/task_list.html', {'tasks': tasks})

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
