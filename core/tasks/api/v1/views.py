# API
"""
from django.http import HttpResponse
def api_task_list_view(request):
    return HttpResponse("ok")
"""

# API function base view
# from rest_framework import mixins,status
from rest_framework import viewsets

# from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter

# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# from rest_framework.response import Response
# from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404


from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPagination
from .filter import TaskFilter
from ...models import Task


"""
# @api_view('GET',)
# @api_view(['GET','POST'])
@api_view()
def api_task_list_view(request):
    return Response({'name':'poorya'})

"""


"""
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def TaskList(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        # tasks = Task.objects.filter(complete=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors)
"""


"""
class TaskList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get(self,request):
        tasks = Task.objects.all()
        # tasks = Task.objects.filter(complete=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
"""


"""
class TaskList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all() #Task.objects.filter(complete=False)
"""

"""
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def taskDetail(request,id):
    task = get_object_or_404(Task,pk=id)
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
        # try:
        #     task = Task.objects.get(pk=id)
        #     serializer = TaskSerializer(task)
        #     return Response(serializer.data)
        # except Task.DoesNotExist:
        #     return Response({'detail':'task does not found'},status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        serializer = TaskSerializer(task,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        task.delete()
        return Response({'detail':'item removed successfuly.'},status=status.HTTP_204_NO_CONTENT)
"""


"""
class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get(self,request,id):
        task = get_object_or_404(Task,pk=id)
        serializer = self.serializer_class(task)
        return Response(serializer.data)
    def put(self,request,id):
        task = get_object_or_404(Task,pk=id)
        serializer = TaskSerializer(task,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,id):
        task = get_object_or_404(Task,pk=id)
        task.delete()
        return Response({'detail':'item removed successfuly.'},status=status.HTTP_204_NO_CONTENT)
"""

"""'
class TaskDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
"""

# Example for ViewSet in CBV

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView

class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    #queryset = Task.objects.all()  # Task.objects.filter(complete=False)
    def get_queryset(self):
        return Task.objects.filter(creator__user=self.request.user)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ["created_date", "due_date"]
    # filterset_fields = ['creator', 'title', 'complete', 'active']
    search_fields = ["title"]
    pagination_class = CustomPagination
    def perform_update(self, serializer):
        serializer.save()


class ActiveUserRequiredMixin(UserPassesTestMixin):
    def test_func(self, *args, **kwargs):
        return self.request.user.is_active


"""
class TasksListApiView(ActiveUserRequiredMixin, TemplateView):
    permission_classes = [IsOwnerOrReadOnly]
    template_name = 'tasks/new_task_list.html'
    # template_name = 'tasks/task_list_api.html'
"""

    
    
class TasksListApiView(viewsets.ModelViewSet, TemplateView):
    # permission_classes = [IsOwnerOrReadOnly]
    template_name = 'tasks/new_task_list.html'
    # template_name = 'tasks/task_list_api.html'
    serializer_class = TaskSerializer
    #queryset = Task.objects.all()  # Task.objects.filter(complete=False)
    def get_queryset(self):
        return Task.objects.filter(creator__user=self.request.user)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ["created_date", "due_date"]
    # filterset_fields = ['creator', 'title', 'complete', 'active']
    search_fields = ["title"]
    pagination_class = CustomPagination
    def perform_update(self, serializer):
        serializer.save()    
    
    

class TasksListUpdateApiView(ActiveUserRequiredMixin, TemplateView):
    template_name = 'tasks/task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('pk')
        context['task'] = get_object_or_404(Task, id=task_id, creator__user=self.request.user)
        return context