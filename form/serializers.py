from rest_framework.serializers import ModelSerializer

from core.serializers import UniversitySerializer, SpecializationSerializer, JobSerializer
from token_auth.serializers import UserProfileSerializer
from vacancy.serializers import SkillSerializer
from .utils import *


class EducationSerializer(ModelSerializer):
    university = UniversitySerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)

    class Meta:
        model = Education
        fields = '__all__'


class FormSerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    educations = EducationSerializer(many=True)
    jobs = JobSerializer(many=True)
    skills = SkillSerializer(many=True, read_only=True)

    def create(self, validated_data):
        educations = validated_data.pop('educations')
        jobs = validated_data.pop('jobs')
        skills = validated_data.pop('skills')

        form = Form.objects.create(**validated_data)

        create_form_educations(form, educations)
        create_form_jobs(form, jobs)
        create_form_skills(form, skills)

        return form

    def update(self, instance, validated_data):
        educations = validated_data.pop('educations')
        jobs = validated_data.pop('jobs')
        skills = validated_data.pop('skills')

        if educations is not None:
            create_form_educations(instance, educations)

        if jobs is not None:
            create_form_jobs(instance, jobs)

        if skills is not None:
            create_form_skills(instance, skills)

        instance.city = validated_data.get('city', instance.city)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.about = validated_data.get('about', instance.about)

        instance.save()

        return instance

    def to_representation(self, obj):
        form = super(FormSerializer, self).to_representation(obj)
        form.pop('profile')

        return form

    class Meta:
        model = Form
        fields = '__all__'
        extra_kwargs = {

        }
