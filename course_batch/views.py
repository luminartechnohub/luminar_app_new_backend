from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import BasicAuthentication 
from rest_framework import status
from rest_framework import generics


from .serializers import ModuleSerializer,CourseSerializer 
from .models import Course,Module
from account.permissions import SuperadminPermission,FacultyPermission,StudentPermission,AdminPermission
from rest_framework import serializers


class CourseRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        if not course:
            response_data = {
                "status": 0,
                "message": "Not found."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        response_data = {
            "status": 1,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CourseCreateView(APIView):
    serializer_class = CourseSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [SuperadminPermission]

    def post(self, request):
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save(is_active=True)
           response_data = {
                "status": 1,
                "data": serializer.data
            }

           return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({"status":0,"message":serializer.errors})
            
class CourseListView(APIView):
    serializer_class = CourseSerializer

    def get(self, request):
       try:
            # Retrieve all courses from the database
           courses = Course.objects.filter(is_active=True)

            # Serialize the courses using the serializer
           serializer = self.serializer_class(courses, many=True)

           total_count = courses.count()

            # Return the serialized data in the response
           response_data={
                'status':1,
                "data":serializer.data,
                "total_results":total_count
            }
           return Response(response_data, status=status.HTTP_200_OK)
       except Exception as e:
           return Response({
               'status':0,
               "message":'Courses not Availabe'
           })

class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [SuperadminPermission]

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_data = {
                "status": 1,
                "data": serializer.data
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "status": 0,
                "message": str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [SuperadminPermission]
    lookup_field = 'pk'  # Specify the lookup field for identifying the course to delete

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"status": 1, "message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"status": 0, "message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)   

class ModuleCreateView(APIView):
    serializer_class = ModuleSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AdminPermission]

    def post(self, request,*args, **kwargs):
        course_id=kwargs.get('pk')
        course_obj=Course.objects.get(id=course_id)
        serializer=ModuleSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save(course=course_obj)
           response_data = {
                "status": 1,
                "data": serializer.data
            }

           return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({"status":0,"message":serializer.errors})
