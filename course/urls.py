from django.urls import path,include
from . import views

urlpatterns = [
    path('student/courses/', views.CourseView.as_view({'get': 'list', 'post': 'create'}), name='course'),
    path('student/courses/<int:pk>/', views.CourseView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='course-detail'),
    path('admin/modules/', views.ModuleView.as_view({'get': 'list', 'post': 'create'}), name='module'),
    path('admin/modules/<int:pk>/', views.ModuleView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='module-detail'),
]