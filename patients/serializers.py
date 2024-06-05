from .models import Patient
from rest_framework import serializers


class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_date', 'created_by']

    def create(self, validated_data):
        print('validated_data is ', validated_data)
        user_info = validated_data.pop('user')
        validated_data['created_by']=user_info
        return super().create(validated_data)

