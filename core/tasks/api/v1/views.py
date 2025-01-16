
   
# API
'''
from django.http import HttpResponse
def api_task_list_view(request):
    return HttpResponse("ok")
'''

# API function base view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from ...models import Task # from tasks.models import Task

# @api_view('GET',)
# @api_view(['GET','POST'])
@api_view()
def api_task_list_view(request):
    return Response({'name':'poorya'})


@api_view()
def TaskList(request):
    return Response({'api':'v1'})


@api_view()
def TaskDetail(request,id):
    task = Task.objects.get(pk=id)
    print(task.__dict__)
    serializer = TaskSerializer(task)
    print (serializer.data)
    return Response(serializer.data)