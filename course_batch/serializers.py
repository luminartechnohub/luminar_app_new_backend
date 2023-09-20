from rest_framework import serializers
from .models import Course,Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'duration', 'offline_fees', 'online_fees', 'thumbnail', 'full_name', 'cochin_date', 'calicut_date', 'is_active','online_active','offline_active')
