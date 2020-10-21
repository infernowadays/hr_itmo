from rest_framework.serializers import ModelSerializer
from .models import University, Specialization


class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'
