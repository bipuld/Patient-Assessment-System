from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .serializers import  PatientsSerializer
from user.models import UserInfo
from .models import Patient
from patients_asse import global_msg
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

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
        """this request handle the Creation of the Patients records associated with Specific login user"""
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


    def get(self,request):
        """this method handle the List all  of the Patients records associated with Specific login user"""
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
        
        patients = Patient.objects.filter(created_by=user_info_instance).order_by('-created_date')
        serializer = PatientsSerializer(patients, many=True)
        messages = {
            'responseCode': global_msg.SUCCESS_RESPONSE_CODE,
            'message': "Patient records fetched successfully.",
            'data': serializer.data
        }
        return JsonResponse(messages, status=status.HTTP_200_OK)
    

    def put(self, request):
        """this method handle the Updating of  all  of the Patients records  with their id passing in the headres associated with Specific login user"""
        patient_id = request.headers.get('patients-id', None)
        print('patient_id is ', patient_id)
        if not patient_id:
            messages = {
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient ID is required for updating the patient record."
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(id=patient_id)
            print('patient is ', patient)
        except Patient.DoesNotExist:
            messages = {
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient record not found."
            }
            return JsonResponse(messages, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientsSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            patient.updated_at = datetime.now()
            patient.save()

            messages = {
                'responseCode': global_msg.SUCCESS_RESPONSE_CODE,
                'message': "Patient record updated successfully.",
                'data': serializer.data
            }
            return JsonResponse(messages, status=status.HTTP_200_OK)
        else:
            messages = {
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Failed to update patient record.",
                'errors': serializer.errors
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        """this method handle the delete the Patients records  with their id passing in the headres associated with Specific login user"""
        patient_id = request.headers.get('patients-id', None)
        print('patient_id is ', patient_id)
        if not patient_id:
            messages = {
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient ID is required for deleting the patient record."
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(id=patient_id)
            print('patient is ', patient)
        except Patient.DoesNotExist:
            messages = {
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient record not found."
            }
            return JsonResponse(messages, status=status.HTTP_404_NOT_FOUND)
        
        patient.delete()
        messages = {
            'responseCode': global_msg.SUCCESS_RESPONSE_CODE,
            'message': "Patient record deleted successfully."
        }
        return JsonResponse(messages, status=status.HTTP_200_OK)