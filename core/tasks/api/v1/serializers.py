from rest_framework import serializers
from ...models import Task

# class TaskSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     complete = serializers.BooleanField()
    
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['id','title', 'complete','active','created_date','due_date']
        