from django.urls import path
from .views import *


urlpatterns = [
    path('', PatientsRecord.as_view(), name='patients_details'),
]