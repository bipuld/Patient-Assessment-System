from .models import Patient
from rest_framework import serializers


class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_date', 'created_by']


    def validate_phone_number(self, value):
        """
        Check if the phone number already exists in the database.
        """
        if Patient.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def create(self, validated_data):
        print('validated_data is ', validated_data)
        user_info = validated_data.pop('user')
        validated_data['created_by']=user_info
        return super().create(validated_data)

