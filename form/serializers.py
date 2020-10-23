from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import *
from token_auth.serializers import UserProfileSerializer
from core.serializers import CitySerializer, UniversitySerializer, SpecializationSerializer


class EducationSerializer(ModelSerializer):
    university = UniversitySerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)

    class Meta:
        model = Education
        fields = '__all__'


class DutySerializer(ModelSerializer):
    class Meta:
        model = Duty
        fields = '__all__'


class JobSerializer(ModelSerializer):
    duties = DutySerializer(many=True)

    class Meta:
        model = Job
        fields = '__all__'


class ExtraSkillSerializer(ModelSerializer):
    class Meta:
        model = ExtraSkill
        fields = '__all__'


class SoftSkillSerializer(ModelSerializer):
    class Meta:
        model = SoftSkill
        fields = '__all__'


class AchievementSerializer(ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'


class FormSerializer(ModelSerializer):
    student = UserProfileSerializer(read_only=True)
    educations = EducationSerializer(many=True)
    jobs = JobSerializer(many=True)
    extra_skills = ExtraSkillSerializer(many=True)
    soft_skills = SoftSkillSerializer(many=True)
    achievements = AchievementSerializer(many=True)

    class Meta:
        model = Form
        fields = '__all__'
