from rest_framework import serializers
from .models import User,Student

class StudentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Student
        fields = ('id','parent_no')  # Include other fields as needed

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'password', 'dob', 'email', 'gender','user_type')

