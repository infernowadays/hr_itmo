from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import *
from company.serializers import CompanySerializer
from token_auth.serializers import UserProfileSerializer
from core.serializers import SpecializationSerializer


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class VacancySerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True, required=False)
    specializations = SpecializationSerializer(read_only=True, many=True)

    class Meta:
        model = Vacancy
        fields = '__all__'

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        specializations = validated_data.pop('specializations')

        vacancy = Vacancy.objects.create(**validated_data)

        if skills is not None:
            for string_skill in skills:
                skill = Skill.objects.filter(text=string_skill.get('text'))

                if not skill:
                    skill = Skill.objects.create(id=string_skill.get('id'), text=string_skill.get('text'))
                else:
                    skill = skill.get()

                VacancySkills.objects.create(vacancy=vacancy, skill=skill)

        if specializations is not None:
            for specialization in specializations:
                VacancySpecializations.objects.create(vacancy_id=vacancy.id, specialization_id=specialization)

        return vacancy


class RequestSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    vacancy = serializers.IntegerField(source='vacancy.id', read_only=True)

    class Meta:
        model = Request
        fields = '__all__'
        extra_kwargs = {'decision': {'required': False}}
