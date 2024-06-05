from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'phone_number', 'date_of_birth', 'age', 'address')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('gender',)

    def age(self, obj):
        from datetime import date
        today = date.today()
        age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
        return age

    age.short_description = 'Age'

