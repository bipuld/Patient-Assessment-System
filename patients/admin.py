from django.contrib import admin
from .models import Patient,Clinician,Assessment


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'phone_number', 'date_of_birth', 'age', 'address','created_by')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('gender',)

    def created_by(self,obj):
        return obj.created_by.user.username

    def age(self, obj):
        from datetime import date
        today = date.today()
        age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
        return age

    age.short_description = 'Age'

@admin.register(Clinician)
class ClinicianAdmin(admin.ModelAdmin):
    list_display = ('clincal_user',)
    search_fields = ('clincal_user',)

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment_type', 'patient', 'assessment_date', 'final_score','clinician')
    list_filter = ('assessment_type', 'assessment_date', 'clinician')
    search_fields = ('assessment_type', 'patient__full_name', 'clinician__full_name') 
    date_hierarchy = 'assessment_date' #d ate_hierarchy to provide a date-based drill-down navigation for assessment_date.
    ordering = ('assessment_date',)