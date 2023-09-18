from rest_framework import serializers
from .models import User,Course,Module
class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('id','full_name','phone','password','parent_no','course_name','dob','email','gender',) 
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"
class CourseSerializer(serializers.ModelSerializer):
    
    modules = ModuleSerializer(many=True,read_only=True) 

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'offline_fees', 'online_fees', 'thumbnail', 'full_name', 'cochin', 'calicut', 'modules']

