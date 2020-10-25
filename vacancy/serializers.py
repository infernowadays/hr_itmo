from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from company.serializers import CompanySerializer
from core.serializers import SpecializationSerializer
from token_auth.serializers import UserProfileSerializer
from .models import *
from .utils import create_skills


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class VacancyShortSerializer(ModelSerializer):
    company_id = serializers.CharField(source='company.id')
    company_name = serializers.CharField(source='company.name')
    company_logo = serializers.CharField(source='company.logo')
    skills = SkillSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Vacancy
        fields = (
            'id', 'short_description', 'description', 'name', 'company_id', 'company_name', 'is_active', 'approved',
            'company_logo', 'skills', 'link', 'external',)


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


class FavouriteVacancySerializer(ModelSerializer):
    vacancy = VacancySerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = VacancyFavorites
        fields = '__all__'


class RequestSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    vacancy = serializers.IntegerField(source='vacancy.id', read_only=True)

    class Meta:
        model = Request
        fields = '__all__'
        extra_kwargs = {'decision': {'required': False}}
