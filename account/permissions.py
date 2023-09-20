from rest_framework import permissions


class SuperadminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'superadmin'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type == 'superadmin'


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['superadmin', 'admin']

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type in ['superadmin', 'admin']


class FacultyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['superadmin', 'admin', 'faculty']

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type in ['superadmin', 'admin', 'faculty']
    
class StudentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['superadmin', 'admin', 'faculty' , 'student']

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type in ['superadmin', 'admin', 'faculty' ,'student']    