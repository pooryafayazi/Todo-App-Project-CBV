
   
# API
'''
from django.http import HttpResponse
def api_task_list_view(request):
    return HttpResponse("ok")
'''

# API function base view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from ...models import Task # from tasks.models import Task
from django.shortcuts import get_object_or_404

# @api_view('GET',)
# @api_view(['GET','POST'])
@api_view()
def api_task_list_view(request):
    return Response({'name':'poorya'})


@api_view(['GET','POST'])
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


@api_view(['GET','PUT'])
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
        