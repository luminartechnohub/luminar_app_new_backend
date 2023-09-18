
from django.urls import path,include
from .views import send_otp,verify_otp
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    
    path('user/register/',send_otp),
    path('user/verify_otp/',verify_otp),
    path('token/',TokenObtainPairView.as_view(),name='obtain_pairview'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('user/login/', views.UserLoginView.as_view(), name='user_login'),
    path('student/courses/',views.CourseSerializer.as_view(),name='course'),
    path('admin/modules/',views.ModuleSerializer.as_view(),name='module'),
]
