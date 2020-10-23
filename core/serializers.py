from rest_framework.serializers import ModelSerializer
from .models import University, Specialization, City


class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
