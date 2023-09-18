from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import send_otp_phone
from .models import User,Course,Module
from .serializers import UserSerializer ,ModuleSerializer,CourseSerializer 
from rest_framework import viewsets


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


# user registration and otp sending

@api_view(['POST'])
def send_otp(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        errors = serializer.errors
        return Response({
            'status': 0,
            'message': 'Validation failed',
            'errors': errors
        })


    phone_number = serializer.validated_data['phone']
    password = serializer.validated_data['password']
    full_name =serializer.validated_data['full_name']
    course_name =serializer.validated_data['course_name']
    parent_no =serializer.validated_data['parent_no']
    dob =serializer.validated_data['dob']
    gender =serializer.validated_data['gender']
    email = serializer.validated_data['email']

    try:
        user = User.objects.get(phone=phone_number)
        # User with this phone number already exists, handle accordingly.
        return Response({
            'status': 0,
            'message': 'Phone number is already registered.'
        })
    except User.DoesNotExist:
        # Create a new user if one with this phone number doesn't exist.
        user = User.objects.create(
            phone=phone_number,
            otp=send_otp_phone(phone_number),
            full_name=full_name,
            course_name=course_name,
            parent_no=parent_no,
            dob=dob,
            gender=gender,
            email=email,
            user_type='student'


        )
        # Set the password using set_password
        user.set_password(password)
        user.save()
        return Response({
            'status': 1,
            'message': 'OTP sent and user created.'
        })


# verifying phone number

@api_view(['POST'])
def verify_otp(request):
    data = request.data

    if data.get('phone') is None:
        return Response({
            'status': 0,
            'message': 'Phone number is required.'
        })

    if data.get('otp') is None:
        return Response({
            'status': 0,
            'message': 'OTP is required.'
        })

    try:
        user_obj = User.objects.get(phone=data.get('phone'))
    except User.DoesNotExist:
        return Response({
            'status': 0,
            'message': 'Invalid phone number.'
        })

    if user_obj.otp == data.get('otp'):
        user_obj.phone_verified = True
        user_obj.save()

        # Generate access and refresh tokens
        refresh = RefreshToken.for_user(user_obj)

        # Include user information and tokens in the response
        response_data = {
            'status': 1,
            'message': 'OTP matched.',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                'user': {
                    'id': user_obj.id,
                    'full_name': user_obj.full_name,
                    'phone': user_obj.phone,
                    'parent_no': user_obj.parent_no,
                    'dob': user_obj.dob,
                    'email': user_obj.email,
                    'gender': user_obj.gender,
                    'phone_verified': user_obj.phone_verified,
                    'user_type':user_obj.user_type
                }
            }
        }
        
        return Response(response_data)
    
    return Response({
        'status': 0,
        'message': 'Invalid OTP.'
    })


current_user = get_user_model()

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        try:
            user = current_user.objects.get(phone=phone,phone_verified=True)  # Corrected filter argument
        except current_user.DoesNotExist:
            return Response({'status':0,'message': 'Invalid phone or password'}, status=400)

        if user.check_password(password):
            if not hasattr(user, 'access_token'):  # Check if the user has an access token
                refresh = RefreshToken.for_user(user)
                user.access_token = str(refresh.access_token)
                user.save()

            return Response({
                'status':1,
                'data':{
                    'token':{
                           'refresh': str(refresh),
                'access': str(refresh.access_token)
                    },
                     'user': {
                    'id': user.id,
                    'full_name': user.full_name,
                    'phone': user.phone,
                    'parent_no': user.parent_no,
                    'dob': user.dob,
                    'email': user.email,
                    'gender': user.gender,
                    'phone_verified': user.phone_verified,
                    'user_type':user.user_type

                }
                }
                 
            
               
            })

        return Response({'status':0,'message': 'Invalid phone or password'}, status=400)
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

