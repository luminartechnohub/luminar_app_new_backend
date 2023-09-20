from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseRetrieveView,CourseCreateView,CourseListView,CourseUpdateView,CourseDeleteView,ModuleCreateView


urlpatterns = [
    path('courses/<int:pk>/', CourseRetrieveView.as_view(), name='course-retrieve'),
    path('courses/create/',CourseCreateView.as_view(),name='create-course'),
    path('courses/list/',CourseListView.as_view(),name='courses-list'),
    path('courses/update/<int:pk>/',CourseUpdateView.as_view(),name='course-update'),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course-delete'),

    path('module/create/<int:pk>/',ModuleCreateView.as_view(),name='module-create'),
    ]


