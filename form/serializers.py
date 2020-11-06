from rest_framework.serializers import ModelSerializer

from core.models import JobDuties
from core.serializers import UniversitySerializer, SpecializationSerializer
from token_auth.serializers import UserProfileSerializer
from vacancy.serializers import SkillSerializer, JobSerializer
from .models import *


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

        for education in educations:
            education['university'] = University.objects.get(pk=education['university'])
            education['specialization'] = Specialization.objects.get(pk=education['specialization'])
            education = Education.objects.create(**education)
            FormEducations.objects.create(form=form, education=education)

        for job in jobs:
            duties = job.pop('duties')
            job = Job.objects.create(**job)
            for duty in duties:
                duty = Duty.objects.create(text=duty)
                JobDuties.objects.create(job=job, duty=duty)
            FormJobs.objects.create(form=form, job=job)

        for skill_text in skills:
            skill = Skill.objects.filter(text=skill_text.get('text'))

            if not skill:
                skill_text = Skill.objects.create(id=skill_text.get('id'), text=skill_text.get('text'))
            else:
                skill_text = skill.get()

            FormSkills.objects.create(form=form, skill=skill_text)

        return form

    def to_representation(self, obj):
        form = super(FormSerializer, self).to_representation(obj)
        form.pop('profile')

        return form

    class Meta:
        model = Form
        fields = '__all__'
