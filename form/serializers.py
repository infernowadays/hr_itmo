from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import *
from token_auth.serializers import UserProfileSerializer
from core.serializers import CitySerializer, UniversitySerializer, SpecializationSerializer
from .models import *


class EducationSerializer(ModelSerializer):
    university = UniversitySerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)

    class Meta:
        model = Education
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


class ExtraSkillSerializer(ModelSerializer):
    class Meta:
        model = ExtraSkill
        fields = '__all__'


class SoftSkillSerializer(ModelSerializer):
    def to_representation(self, value):
        return value.text

    class Meta:
        model = SoftSkill
        fields = '__all__'


class AchievementSerializer(ModelSerializer):
    def to_representation(self, value):
        return value.text

    class Meta:
        model = Achievement
        fields = '__all__'


class FormSerializer(ModelSerializer):
    student = UserProfileSerializer(read_only=True)
    educations = EducationSerializer(many=True)
    jobs = JobSerializer(many=True)
    extra_skills = ExtraSkillSerializer(many=True, read_only=True, required=False)
    soft_skills = SoftSkillSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)

    def create(self, validated_data):
        educations = validated_data.pop('educations')
        jobs = validated_data.pop('jobs')
        extra_skills = validated_data.pop('extra_skills')
        soft_skills = validated_data.pop('soft_skills')
        achievements = validated_data.pop('achievements')

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

        for extra_skill in extra_skills:
            extra_skill_obj = ExtraSkill.objects.filter(text=extra_skill.get('text'))

            if not extra_skill_obj:
                extra_skill = ExtraSkill.objects.create(id=extra_skill.get('id'), text=extra_skill.get('text'))
            else:
                extra_skill = extra_skill.get()

            FormExtraSkills.objects.create(form=form, extra_skill=extra_skill)

        for soft_skill in soft_skills:
            soft_skill = SoftSkill.objects.create(text=soft_skill)
            FormSoftSkills.objects.create(form=form, soft_skill=soft_skill)

        for achievement in achievements:
            achievement = Achievement.objects.create(text=achievement)
            FormAchievements.objects.create(form=form, achievement=achievement)

        return form

    class Meta:
        model = Form
        fields = '__all__'
