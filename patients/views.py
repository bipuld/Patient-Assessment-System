from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .serializers import  PatientsSerializer
from .models import UserInfo
from patients_asse import global_msg
from rest_framework.permissions import IsAuthenticated




class PatientsRecord(APIView):
    """
    API endpoint for creating a new patient record.

    Method: POST
    Parameters (JSON Body):
        - full_name (str): The patient's full name. (Required)
        - gender (str): The patient's gender. (Required)
        - phone_number (str): The patient's phone number. (Required)
        - date_of_birth (str): The patient's date of birth (YYYY-MM-DD). (Required)
        - address (str): The patient's address. (Required)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            messages = {
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "No data provided in the request body."
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        print('request.user so current user is ', user)
        try:
            user_info_instance = UserInfo.objects.get(user=user)
            print('User info so current user is ', user_info_instance)
        except UserInfo.DoesNotExist:
            messages = {
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "User profile not found."
            }
            return JsonResponse(messages, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user_info_instance)
            messages = {
                'responseCode': global_msg.SUCCESS_RESPONSE_CODE,
                'message': "Patient record created successfully."
            }
            return JsonResponse(messages, status=status.HTTP_201_CREATED)

        messages = {
            'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
            'message': "Failed to create patient record.",
            'errors': serializer.errors
        }
        return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)
