from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CourseRetrieveView,CourseCreateView,CourseListView,CourseUpdateView,
                    CourseDeleteView,ModuleCreateView,ModuleUpdateView,ModuleDeleteView,
                    BatchCreateView,BatchListView,BatchUpdateView,BatchDeleteView)


urlpatterns = [
    path('courses/<int:pk>/', CourseRetrieveView.as_view(), name='course-retrieve'),
    path('courses/create/',CourseCreateView.as_view(),name='create-course'),
    path('courses/list/',CourseListView.as_view(),name='courses-list'),
    path('courses/update/<int:pk>/',CourseUpdateView.as_view(),name='course-update'),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course-delete'),

    path('module/create/<int:pk>/',ModuleCreateView.as_view(),name='module-create'),
    path('module/update/<int:pk>/',ModuleUpdateView.as_view(),name='module-update'),
    path('module/delete/<int:pk>/', ModuleDeleteView.as_view(), name='course-delete'),

    path('batches/create/<int:pk>/',BatchCreateView.as_view(),name='batch-create'),
    path('batches/list/', BatchListView.as_view(), name='batch-list'),
    path('batches/update/<int:pk>/',BatchUpdateView.as_view(),name='batch-update'),
    path('batches/delete/<int:pk>/',BatchDeleteView.as_view(),name='batch-delete'),


    ]


