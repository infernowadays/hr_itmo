from rest_framework.serializers import ModelSerializer
from .models import University, Specialization


class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University


class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
