from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('id','full_name','phone','password','parent_no','course_name','dob','email','gender',) 
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
