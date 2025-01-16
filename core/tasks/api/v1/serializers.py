from rest_framework import serializers
from ...models import Task

# class TaskSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     complete = serializers.BooleanField()
    
    
class TaskSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField()
    # user = serializers.CharField(read_only=True)
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url =serializers.ReadOnlyField(source='get_absolute_api_url',read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_ur')
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['user','id','title','snippet', 'complete','active','relative_url','absolute_url','created_date','due_date']
        # read_only_fields = ['user']
                
    # def get_absolute_url(self,obj):
    def get_abs_ur(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
        