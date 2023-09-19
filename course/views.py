from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course,Module
from .serializers import ModuleSerializer,CourseSerializer 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    http_method_names=["post","get","put"]
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = {
                "status": "ok",
                "data": serializer.data
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e)
            }
            return Response(response_data)
    def list(self, request, *args, **kwargs): 
        try:
            details = self.get_queryset()
            total_results = details.count()

            if total_results == 0:
                response_data = {
                    "status": "ok",
                    "message": [],
                    "totalResults": total_results
                }
            else:
                serialized_details = self.serializer_class(details, many=True)
                response_data = {
                    
                    "status": "ok",
                    "data": serialized_details.data,
                    "totalResults": total_results
                }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e),
                "totalResults": 0 
            }

        return Response(response_data)
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_data = {
                "status": "ok",
                "data": serializer.data
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e)
            }
            return Response(response_data)
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                "status": "ok",
                "data": serializer.data
            }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e)
            }

        return Response(response_data)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response_data = {
                "status": "ok",
                "message": "Successfully deleted the object.",
            }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e),
            }

        return Response(response_data)
class ModuleView(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    http_method_names=['get','post','put']
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            response_data = {
                "status": "ok",
                "data": serializer.data
            }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e)
            }

        return Response(response_data)
    def list(self, request, *args, **kwargs):
        try:
            user_profiles = self.get_queryset()
            total_results = user_profiles.count()

            if total_results == 0:
                response_data = {
                    "status": "ok",
                    "message": "[]",
                    "totalResults": total_results
                }
            else:
                serialized_user_profiles = self.serializer_class(user_profiles, many=True)
                response_data = {
                    "status": "ok",
                    "data": serialized_user_profiles.data,
                    "totalResults": total_results
                }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e),
                "totalResults": total_results
            }

        return Response(response_data)
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                "status": "ok",
                "data": serializer.data
            }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e)
            }

        return Response(response_data)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            response_data = {
                "status": "ok",
                "data": serializer.data
            }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e)
            }

        return Response(response_data)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response_data = {
                "status": "ok",
                "message": "Successfully deleted the object.",
            }
        except Exception as e:
            response_data = {
                "status": "error",
                "error_message": str(e),
            }

        return Response(response_data)


