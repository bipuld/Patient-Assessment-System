import json
import logging

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserInfo
from .serializers import UserInfoSerializer
from patients_asse import global_msg
from rest_framework_simplejwt.exceptions import TokenError
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from .serializers import UserInfoSerializer


from django.http import JsonResponse
from rest_framework import status
from .serializers import UserInfoSerializer

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserInfo
from django.contrib.auth.models import User


logger=logging.getLogger('django')

@api_view(['POST'])
def signup(request):
    """
    API endpoint for user signup.
    Method: POST
    Parameters:
        - gender (str): The gender of the user. 
        - phone (str): The user's phone number. 
        - first_name (str): The user's first name. 
        - last_name (str): The user's last name. 
        - email (str): The user's email address. 
        - password (str): The user's password. 
        - is_verify (bool): Whether the user's account is verified. (Optional, defaults to False)
    Returns:
        Response object with JSON data:
            - success message on successful creation (status: 201)
            - error message with details on failure (status: 400)
    """

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    try:
        # Create a new User instance
        user = User.objects.create_user(
            username=request.data['email'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name']
        )
    except IntegrityError:
        return JsonResponse({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)


    user_info_serializer = UserInfoSerializer(data=request.data)
    if user_info_serializer.is_valid():
        user_info_serializer.save(user=user)  
        return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        user.delete()  # If UserInfo creation fails, it delete the user instance to maintain data integrity
        return JsonResponse(user_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    """
    API endpoint for user login. This allow us to Login the user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Log in the user.
        Method: POST
        Parameters:
        - username (str): The username of the user.
        - password (str): The password of the user.=
        Returns:
        - JsonResponse: JSON response with user data (username , refresh_token,access_token )orerror message.
        """
        try:
            username = request.data['email'].lower()
            password = request.data['password']
        except KeyError as e:
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: 'Missing username or password in request data.',
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_info_details = UserInfo.objects.filter(user=user).first()
            if user_info_details is None:
                messages = {
                    global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.ERROR_KEY: 'User information not found.',
                }
                return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            messages = {
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return JsonResponse(messages, status=status.HTTP_200_OK)
        else:
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: 'Invalid username or password.',
            }
            return JsonResponse(messages, status=status.HTTP_401_UNAUTHORIZED)


class LogoutApiView(APIView):
    """
    API endpoint for user logout.
    This allow us to logout the user so to logout the authenticating user 
    acess_token of specific user is Authorization :In Bearer Token of Auth_type the acess_token is used to authenticate specific user throgh request.user .
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        Log out the user.
        Method: POST
        Returns:
        - JsonResponse: JSON response with success message or error message.
        """
        user = request.user
        try:
            token = RefreshToken.for_user(user)
            token.blacklist()
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.SUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: "Refresh token revoked successfully."
            }
        except Token as e:
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: str(e)
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)

        print("User Logged Out", user.username)
        user_data = UserInfo.objects.filter(user=user).first()
        if user_data:
            user_fields = {
                'username': user_data.user.username,
                'full_name': f"{user_data.first_name} {user_data.last_name}",
                'email': user_data.email,
            }
        else:
            user_fields = {}
        messages = {
            global_msg.RESPONSE_CODE_KEY: global_msg.SUCCESS_RESPONSE_CODE,
            global_msg.RESPONSE_MESSAGE_KEY: "User logged out successfully",
            global_msg.RESULT_DATA: user_fields
        }
        return JsonResponse(messages, status=status.HTTP_200_OK)


class GetUserProfile(APIView):
    """
    API endpoint for retrieving user profile.
    From the login Api:acess_token of specific user is Authorization :In Bearer Token of Auth_type the acess_token is used to authenticate specific user throgh request.user .
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve user profile.
        Method: GET
        Returns:
        - JsonResponse: JSON response with user profile data or error message.
        """
        user_detail = request.user
        try:
            user_data = UserInfo.objects.get(user=user_detail)
        except UserInfo.DoesNotExist:
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: 'User profile not found',
            }
            return JsonResponse(messages, status=status.HTTP_200_OK)

        profile_data = {
            "username": user_data.user.username,
            "email": user_data.email,
            "full_name": f"{user_data.first_name} {user_data.last_name}",
            "phone": user_data.phone,
        }
        return JsonResponse(profile_data, status=status.HTTP_200_OK)
