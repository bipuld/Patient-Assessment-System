from django.http import JsonResponse
from rest_framework import status
from .serializers import  PatientsSerializer,ClinicianSerializer,AssessmentSerializer
from user.models import UserInfo
from .models import Patient,Clinician,Assessment
from patients_asse import global_msg
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view,APIView,permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ClinicianListAPI(request):
    '''
    Get the list of clinicians.
    '''
    clinicians = Clinician.objects.all()
    # print(":clinicians",clinicians)
    serializer = ClinicianSerializer(clinicians, many=True)
    return JsonResponse(serializer.data, safe=False,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PatientGetClincianAPI(request):
    """
    Get the patients associated with the clinician that is linked to the authenticated user.
    """
    user = request.user
    response_data = {
        'clinician_id': None,
        'clinician_user_id': None,
        'patients': []
    }


    try:
        user_info_instance = UserInfo.objects.get(user=user)
    except UserInfo.DoesNotExist:
        return JsonResponse({
            'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
            'message': "User profile not found."
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        clinician = Clinician.objects.get(clincal_user=user_info_instance)
        response_data['clinician_id'] = clinician.id
        response_data['clinician_user_id'] = clinician.clincal_user.user.id

    except Clinician.DoesNotExist:
        return JsonResponse({
            'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
            'message': "Clinician record not found"
        }, status=status.HTTP_404_NOT_FOUND)

    patients = Patient.objects.filter(created_by=clinician.clincal_user).order_by('-created_date') 
    for patient in patients:
        response_data['patients'].append({
            'id': patient.id,
            'full_name': patient.full_name,
            'phone_number': patient.phone_number,
            'date_of_birth': patient.date_of_birth,
            'address': patient.address
        })

    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

class PatientsRecordApiView(APIView):
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
        """
        Update the patient record associated with the logged-in user.

        Method: PUT
        Parameters:
            - patients-id (int): The ID of the patient record to be updated (in headers).
            - Full Patient Record (JSON Body): The updated patient record data.

        Returns:
            - 200 OK: If the patient record is updated successfully.
            - 400 BAD REQUEST: If patient ID is missing or data is invalid.
            - 403 FORBIDDEN: If the user is not authorized to update the patient record.
            - 404 NOT FOUND: If the patient record does not exist.
        """
        patient_id = request.headers.get('patients-id')
        user_info_instance=UserInfo.objects.get(user=request.user)
        if not patient_id:
            return JsonResponse({
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient ID is required for updating the patient record."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return JsonResponse({
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient record not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if patient.created_by != user_info_instance:
            return JsonResponse({
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "You are not authorized to update this patient record."
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PatientsSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            patient.updated_at = timezone.now()
            patient.save()

            return JsonResponse({
                'responseCode': global_msg.SUCCESS_RESPONSE_CODE,
                'message': "Patient record updated successfully.",
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Failed to update patient record.",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        """
        Delete the patient record associated with the logged-in user.

        Method: DELETE
        Parameters:
            - patients-id (int): The ID of the patient record to be deleted (in headers).

        Returns:
            - 200 OK: If the patient record is deleted successfully.
            - 400 BAD REQUEST: If patient ID is missing or data is invalid.
            - 403 FORBIDDEN: If the user is not authorized to delete the patient record.
            - 404 NOT FOUND: If the patient record does not exist.
        """
        patient_id = request.headers.get('patients-id')
        user=request.user
        user_info_instance=UserInfo.objects.get(user=user)
        if not patient_id:
            return JsonResponse({
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient ID is required for deleting the patient record."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return JsonResponse({
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "Patient record not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if patient.created_by != user_info_instance:
            return JsonResponse({
                'responseCode': global_msg.UNSUCCESS_RESPONSE_CODE,
                'message': "You are not authorized to delete this patient record."
            }, status=status.HTTP_403_FORBIDDEN)
        
        patient.delete()
        
        return JsonResponse({
            'responseCode': global_msg.SUCCESS_RESPONSE_CODE,
            'message': "Patient record deleted successfully."
        }, status=status.HTTP_200_OK)

class AssessmentApiView(APIView):
    """This class enables assessment CRUD operations, leveraging relationships between clinicians, patients, and user information"""
    permission_classes = [IsAuthenticated]

    def post(self,request):
        clinician_id = request.headers.get('clinician-id')
        user=request.user
        patient_id = request.headers.get('patient-id')

        if not clinician_id or not patient_id:
            return JsonResponse({
                'responseCode': '400',
                'message': 'Failed to create assessment record.',
                'errors': {
                    'clinician': ['Clinician ID is required.'],
                    'patient': ['Patient ID is required.']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:   
            clinician = Clinician.objects.get(id=clinician_id)
            patient = Patient.objects.get(id=patient_id, created_by=clinician.clincal_user)
        except Clinician.DoesNotExist:
            return JsonResponse({
                'responseCode': '404',
                'message': 'Clinician record not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return JsonResponse({
                'responseCode': '404',
                'message': 'Patient record not found or not associated with the specified clinician.'
            }, status=status.HTTP_404_NOT_FOUND)

        
        serializer = AssessmentSerializer(data=request.data,context={'clinician': clinician, 'patient': patient})
        # print(serializer)
        # serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the assessment record with associated clinician and patient
            # print('serialzers',serializer)
            serializer.save()
            return JsonResponse({
                'responseCode': '200',
                'message': f'Assessment record created successfully for patient: {patient.full_name} and clinician: {clinician.clincal_user.user.username}'
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                'responseCode': '400',
                'message': 'Failed to create assessment record.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Getting filter parameters from query parameters
        assessment_type = request.query_params.get('assessment_type')
        assessment_date = request.query_params.get('assessment_date')
        patient_id = request.query_params.get('patient_id')
        clinician_id = request.headers.get('clinician-id')

        print('assessment_type',assessment_type)
        print('assessment_date',assessment_date)
        print('patient_id',patient_id)
  
        assessments = Assessment.objects.filter(clinician_id=clinician_id).order_by('assessment_date')
        print('assessments',assessments)

 
        if assessment_type:
            assessments = assessments.filter(assessment_type=assessment_type)
            print('assessments 1',assessments)

        if assessment_date:
            assessments = assessments.filter(assessment_date=assessment_date)
            print('assessments 2',assessments)

        if patient_id:
            assessments = assessments.filter(patient=patient_id)
            print('assessments 3',assessments)

        paginator = Paginator(assessments,2)
        page_num = request.query_params.get('page')
        # print('page_num',page_num)

        try:
            paginated_assessments = paginator.page(page_num)
        except PageNotAnInteger: #IF page quesry is not integer then it give first page 
            paginated_assessments = paginator.page(1)
        except EmptyPage: # page is out of range (e.g. 9999), deliver last page of results.
            paginated_assessments = paginator.page(paginator.num_pages)

               
       
        serializer = AssessmentSerializer(paginated_assessments, many=True)

        return JsonResponse({
            'responseCode': global_msg.SUCCESS_RESPONSE_CODE,
            'message': 'Assessment records fetched successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)