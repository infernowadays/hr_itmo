from django.db import models

from core.models import City, University, Specialization
from core.models import Skill, Job, Duty
from token_auth.models import UserProfile


class Education(models.Model):
    graduate_year = models.IntegerField(null=False, blank=False)
    university = models.ForeignKey(University, null=False, blank=False, db_constraint=True, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, null=False, blank=False, db_constraint=True,
                                       on_delete=models.CASCADE)

    class Meta:
        db_table = 'education'


class Form(models.Model):
    city = models.CharField(max_length=128, null=True, blank=True)
    profile = models.ForeignKey(UserProfile, null=False, db_constraint=True, on_delete=models.CASCADE,
                                related_name='form')

    about = models.TextField(null=True, blank=True)
    educations = models.ManyToManyField(Education, through='FormEducations', blank=True)
    jobs = models.ManyToManyField(Job, through='FormJobs')
    skills = models.ManyToManyField(Skill, through='FormSkills')

    vk = models.CharField(max_length=128, null=True, blank=True)
    telegram = models.CharField(max_length=128, null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    linkedin = models.CharField(max_length=128, null=True, blank=True)
    website = models.CharField(max_length=128, null=True, blank=True)
    github = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'form'


class FormEducations(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)
    education = models.ForeignKey(Education, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'form_educations'


class FormJobs(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'form_jobs'


class FormSkills(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'form_skills'
