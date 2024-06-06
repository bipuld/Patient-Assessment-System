from .models import Patient
from rest_framework import serializers

from .models import Clinician, Patient, Assessment

class ClinicianSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='clincal_user.user.email')
    class Meta:
        model = Clinician
        fields = ['id', 'email']

        
class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_date', 'created_by']


    def validate_phone_number(self, value):
        """
        Check if the phone number already exists in the our record.
        """
        if Patient.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def create(self, validated_data):
        print('validated_data is ', validated_data)
        user_info = validated_data.pop('user')
        validated_data['created_by']=user_info
        return super().create(validated_data)



class AssessmentSerializer(serializers.ModelSerializer):
    clinician_id = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    class Meta:
        model = Assessment
        fields = ['assessment_type', 'assessment_date', 'questions_and_answers', 'final_score','clinician_id', 'patient_id']


    def get_clinician_id(self, obj):
        return obj.clinician.id if obj.clinician else None

    def get_patient_id(self, obj):
        return obj.patient.id if obj.patient else None
    
    def validate(self, attrs):
        clinician = self.context.get('clinician')
        patient = self.context.get('patient')
        if clinician:
            attrs['clinician'] = clinician
        if patient:
            attrs['patient'] = patient

        return attrs