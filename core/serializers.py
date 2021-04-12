from rest_framework.serializers import ModelSerializer

from .models import *


class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class SkillSerializer(ModelSerializer):
    def to_representation(self, skill):
        return skill.text

    class Meta:
        model = Skill
        fields = '__all__'


class DutySerializer(ModelSerializer):
    def to_representation(self, value):
        return value.text

    class Meta:
        model = Duty
        fields = '__all__'


class JobSerializer(ModelSerializer):
    duties = DutySerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = '__all__'


class LandingSerializer(ModelSerializer):
    class Meta:
        model = Landing
        fields = '__all__'


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
