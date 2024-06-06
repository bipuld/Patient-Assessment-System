from django.urls import path
from .views import *


urlpatterns = [
    path('', PatientsRecordApiView.as_view(), name='patients_details'),
    path('api/ClinicianCreate/',ClinicianCreateAPI,name='create_clinician'),
    path('api/ListClinician/',ClinicianListAPI,name='get_Clinician'),
    path('api/patient-clinician/', PatientGetClincianAPI, name='patient_clinician'),
    path('api/assessment/',AssessmentApiView.as_view(),name='assessment_details')
]