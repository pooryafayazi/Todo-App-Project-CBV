from rest_framework import serializers
from ...models import Task
from accounts.models import User, Profile

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
    # user = serializers.SlugRelatedField(many=False,slug_field='email',queryset=User.objects.all())

    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['creator','id','title','snippet', 'complete','active','relative_url','absolute_url','created_date','due_date']
        read_only_fields = ['creator','active']
                
    # def get_absolute_url(self,obj):
    def get_abs_ur(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    def to_representation(self, instance):
        request = self.context.get('request')
        # print(request.__dict__)
        
        representation = super().to_representation(instance)
        # representation['state'] = 'list'
        if request.parser_context.get('kwargs').get('pk'):
            # representation['state'] = 'single'
            representation.pop('snippet',None)
            representation.pop('relative_url',None)
            representation.pop('absolute_url',None)
        else:
            representation.pop('title',None)
            representation.pop('due_date',None)
        return representation
        
    '''
    def create (self, validated_data):
        validated_data['user'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
    '''
    def create(self, validated_data):
        complete = validated_data.get('complete', False)
        if complete:
            validated_data['active'] = False
        
        validated_data['creator'] = Profile.objects.get(user__id=self.context.get('request').user.id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        complete = validated_data.get('complete', instance.complete)
        if complete:
            validated_data['active'] = False
        else:
            validated_data['active'] = True

        return super().update(instance, validated_data)