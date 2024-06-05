from django.urls import path
from .views import *


urlpatterns = [
    path('', PatientsRecordApiView.as_view(), name='patients_details'),
    path('api/ListClinician/',ClinicianGetAPI,name='Get_Clinician'),
    path('api/assessment/',AssessmentApiView.as_view(),name='assessment_details')
]