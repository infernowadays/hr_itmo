from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from company.serializers import CompanySerializer
from core.models import Duty
from core.serializers import SkillSerializer, JobSerializer, JobDuties
from token_auth.serializers import UserProfileSerializer
from .models import *
from .utils import create_skills


class VacancyShortSerializer(ModelSerializer):
    company_id = serializers.CharField(source='company.id')
    company_name = serializers.CharField(source='company.name')
    company_logo = serializers.CharField(source='company.logo')
    skills = SkillSerializer(many=True, read_only=True, required=False)
    jobs = JobSerializer(many=True)
    schedule_type = serializers.CharField()
    employment_type = serializers.CharField()

    class Meta:
        model = Vacancy
        fields = (
            'id', 'description', 'name', 'company_id', 'company_name', 'is_active', 'approved',
            'company_logo', 'skills', 'jobs', 'schedule_type', 'employment_type',)


class VacancySerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True, required=False)
    jobs = JobSerializer(many=True)

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        jobs = validated_data.pop('jobs')
        vacancy = Vacancy.objects.create(**validated_data)

        if skills is not None:
            create_skills(skills, vacancy)

        for job in jobs:
            duties = job.pop('duties')
            job = Job.objects.create(**job)
            for duty in duties:
                duty = Duty.objects.create(text=duty)
                JobDuties.objects.create(job=job, duty=duty)
            VacancyJobs.objects.create(vacancy=vacancy, job=job)

        return vacancy

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
