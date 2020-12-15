from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from company.serializers import CompanySerializer, CitySerializer
from core.serializers import SkillSerializer, JobSerializer
from token_auth.serializers import UserProfileSerializer
from .models import *
from .utils import create_vacancy_skills


class VacancyShortSerializer(ModelSerializer):
    company_id = serializers.CharField(source='company.id')
    company_name = serializers.CharField(source='company.name')
    company_logo = serializers.CharField(source='company.logo')
    city = CitySerializer(source='company.city')
    skills = SkillSerializer(many=True, read_only=True, required=False)
    # jobs = JobSerializer(many=True)
    schedule_type = serializers.CharField()
    employment_type = serializers.CharField()

    class Meta:
        model = Vacancy
        fields = (
            'id', 'description', 'short_description', 'salary', 'partnership', 'name', 'company_id', 'company_name',
            'is_active', 'approved', 'company_logo', 'skills', 'schedule_type', 'employment_type', 'experience_type',
            'city',)


class VacancySerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True, required=False)

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        vacancy = Vacancy.objects.create(**validated_data)

        create_vacancy_skills(vacancy, skills)

        return vacancy

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        jobs = validated_data.pop('jobs')

        if skills is not None:
            create_vacancy_skills(instance, skills)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.schedule_type = validated_data.get('schedule_type', instance.schedule_type)
        instance.experience_type = validated_data.get('experience_type', instance.experience_type)
        instance.employment_type = validated_data.get('employment_type', instance.employment_type)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.partnership = validated_data.get('partnership', instance.partnership)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        instance.save()

        return instance

    def to_representation(self, obj):
        vacancy = super(VacancySerializer, self).to_representation(obj)
        vacancy.pop('company')

        return vacancy

    class Meta:
        model = Vacancy
        fields = '__all__'


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
