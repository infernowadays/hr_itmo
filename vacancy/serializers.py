from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import *
from company.serializers import CompanySerializer
from token_auth.serializers import UserProfileSerializer
from core.serializers import SpecializationSerializer
from .utils import create_skills


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class VacancySerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True, required=False)
    specializations = SpecializationSerializer(read_only=True, many=True)
    courses = CourseSerializer(many=True)

    class Meta:
        model = Vacancy
        fields = '__all__'

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        specializations = validated_data.pop('specializations')
        courses = validated_data.pop('courses')

        vacancy = Vacancy.objects.create(**validated_data)

        if skills is not None:
            create_skills(skills, vacancy)

        if specializations is not None:
            for specialization in specializations:
                VacancySpecializations.objects.create(vacancy_id=vacancy.id, specialization_id=specialization)

        if courses is not None:
            for course in courses:
                course = Course.objects.create(**course)
                VacancyCourses.objects.create(vacancy=vacancy, course=course)

        return vacancy


class RequestSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    vacancy = serializers.IntegerField(source='vacancy.id', read_only=True)

    class Meta:
        model = Request
        fields = '__all__'
        extra_kwargs = {'decision': {'required': False}}
