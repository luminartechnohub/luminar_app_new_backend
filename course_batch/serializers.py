from rest_framework import serializers
from .models import Course,Module,Batch


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True,read_only=True) 
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'duration', 'offline_fees', 'online_fees', 'thumbnail', 'full_name', 'cochin_date', 'calicut_date', 'is_active','online_active','offline_active','modules')


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch
        fields = "__all__"