from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import MessageHandler
from .models import User,Student
from .serializers import UserSerializer,StudentSerializer


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

import random

@api_view(['POST'])
def send_otp(request):
    # Deserialize the incoming data using UserSerializer
    serializer = UserSerializer(data=request.data)
    
    # Validate the serializer
    if not serializer.is_valid():
        errors = serializer.errors
        return Response({
            'status': 0,
            'message': 'Validation failed',
            'errors': errors
        })

    # Extract validated data from the serializer
    phone_number = serializer.validated_data['phone']
    password = serializer.validated_data['password']
    full_name = serializer.validated_data['full_name']
    dob = serializer.validated_data['dob']
    gender = serializer.validated_data['gender']
    email = serializer.validated_data.get('email', None)  # Email is optional
    user_type = serializer.validated_data.get('user_type','student')  # Default to 'student'

    # Check if a user with this phone number already exists
    try:
        user = User.objects.get(phone=phone_number)
        return Response({
            'status': 0,
            'message': 'Phone number is already registered.'
        })
    except User.DoesNotExist:
        # Generate a random OTP
        current_otp = random.randint(1000, 9999)

        # Create a new User instance
        user = User.objects.create(
            phone=phone_number,
            otp=current_otp,
            full_name=full_name,
            dob=dob,
            gender=gender,
            email=email,
            user_type=user_type
        )
        try:
            message_handler = MessageHandler(phone_number, current_otp)
            message_handler.send_otp_on_phone()
        except Exception as e:
            print(str(e))
        # Set the password using set_password
        user.set_password(password)
        user.save()

        # Create a Student instance associated with the user if the user type is 'student'
        if user_type == 'student':
    
            student_serializer = StudentSerializer(data=request.data)
            
            if student_serializer.is_valid():
                usr_obj=User.objects.get(phone=phone_number)
                parent_no = student_serializer.validated_data['parent_no']
                student_serializer.save(user=usr_obj,parent_no=parent_no)
            else:
                # Handle validation errors for the student data
                return Response({
                    'status': 0,
                    'message': 'Student data validation failed',
                    'errors': student_serializer.errors
                })

        # Send OTP via message_handler (you need to implement this)
        return Response({
            'status': 1,
            'message': 'OTP sent, user created, and student instance created (if applicable).'
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
                    'dob': user_obj.dob,
                    'email': user_obj.email,
                    'gender': user_obj.gender,
                    'phone_verified': user_obj.phone_verified,
                    'user_type':user_obj.user_type,
                    'is_active':user_obj.is_active
                }
            }
        }
        if user_obj.user_type == 'student':
            try:
                student = Student.objects.get(user=user_obj)
                response_data['data']['user']['student_id'] = student.id
                response_data['data']['user']['parent_no'] = student.parent_no
            except Student.DoesNotExist:
                pass  # Handle the case where there is no associated student profile

        
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
            user = User.objects.get(phone=phone, phone_verified=True)
        except User.DoesNotExist:
            return Response({'status': 0, 'message': 'Invalid phone or password'}, status=400)

        if user.check_password(password):
            if not hasattr(user, 'access_token'):
                refresh = RefreshToken.for_user(user)
                user.access_token = str(refresh.access_token)
                user.save()

            response_data = {
                'status': 1,
                'data': {
                    'token': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    'user': {
                        'id': user.id,
                        'full_name': user.full_name,
                        'phone': user.phone,
                        'dob': user.dob,
                        'email': user.email,
                        'gender': user.gender,
                        'phone_verified': user.phone_verified,
                        'user_type': user.user_type,
                        'is_active':user.is_active
                    }
                }
            }

            # If the user is of type 'student', include additional data in the response
            if user.user_type == 'student':
                try:
                    student = Student.objects.get(user=user)
                    response_data['data']['user']['student_id'] = student.id
                    response_data['data']['user']['parent_no'] = student.parent_no
                except Student.DoesNotExist:
                    pass  # Handle the case where there is no associated student profile

            return Response(response_data)

        return Response({'status': 0, 'message': 'Invalid phone or password'}, status=400)