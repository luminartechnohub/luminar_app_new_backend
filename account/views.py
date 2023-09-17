from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import send_otp_phone
from .models import User
from .serializers import UserSerializer  


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
