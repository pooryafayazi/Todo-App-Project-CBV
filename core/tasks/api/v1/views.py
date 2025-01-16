
   
# API
'''
from django.http import HttpResponse
def api_task_list_view(request):
    return HttpResponse("ok")
'''

# API function base view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from ...models import Task # from tasks.models import Task
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

# @api_view('GET',)
# @api_view(['GET','POST'])
@api_view()
def api_task_list_view(request):
    return Response({'name':'poorya'})

'''
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
'''

class TaskList(APIView):
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
        



@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def TaskDetail(request,id):
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
        