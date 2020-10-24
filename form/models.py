from django.db import models

from django.db import models
from token_auth.models import UserProfile
from core.models import City, University, Specialization


class Education(models.Model):
    started = models.CharField(max_length=16, null=False, blank=False)
    ended = models.CharField(max_length=16, null=False, blank=False)
    university = models.ForeignKey(University, null=False, db_constraint=True, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, null=False, db_constraint=True, on_delete=models.CASCADE)
    is_extra = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        db_table = 'education'


class Duty(models.Model):
    text = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'duty'


class Job(models.Model):
    started = models.CharField(max_length=16, null=False, blank=False)
    ended = models.CharField(max_length=16, null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    duties = models.ManyToManyField(Duty, through='JobDuties')

    class Meta:
        db_table = 'job'


class JobDuties(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'job_duties'


class ExtraSkill(models.Model):
    text = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'extra_skill'


class SoftSkill(models.Model):
    text = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'soft_skill'


class Achievement(models.Model):
    text = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'achievement'


class Form(models.Model):
    aim = models.TextField(null=False, blank=False)

    student = models.ForeignKey(UserProfile, null=False, db_constraint=True, on_delete=models.CASCADE,
                                related_name='form')

    educations = models.ManyToManyField(Education, through='FormEducations')
    jobs = models.ManyToManyField(Job, through='FormJobs')

    extra_skills = models.ManyToManyField(ExtraSkill, through='FormExtraSkills')
    soft_skills = models.ManyToManyField(SoftSkill, through='FormSoftSkills')
    achievements = models.ManyToManyField(Achievement, through='FormAchievements')

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


class FormExtraSkills(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)
    extra_skill = models.ForeignKey(ExtraSkill, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'form_extra_skills'


class FormSoftSkills(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)
    soft_skill = models.ForeignKey(SoftSkill, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'form_soft_skills'


class FormAchievements(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'form_achievements'
