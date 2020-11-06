from django.db import models

from company.models import Company
from form.models import Job
from token_auth.models import UserProfile
from .enums import *
from core.models import Skill


class Vacancy(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    schedule_type = models.IntegerField(null=False, blank=False)
    employment_type = models.IntegerField(null=False, blank=False)
    approved = models.BooleanField(null=False, blank=False, default=False)
    partnership = models.TextField(null=False, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    skills = models.ManyToManyField(Skill, through='VacancySkills')
    jobs = models.ManyToManyField(Job, through='VacancyJobs')
    company = models.ForeignKey(Company, null=False, db_constraint=True, on_delete=models.CASCADE,
                                related_name='vacancies')

    class Meta:
        db_table = 'vacancy'


class VacancySkills(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'vacancy_skills'


class VacancyJobs(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'vacancy_jobs'
        unique_together = ['vacancy', 'job']


class VacancyFavorites(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'vacancy_favorites'
        unique_together = ['vacancy', 'user']


class Request(models.Model):
    comment = models.TextField(null=True, blank=True)
    decision = models.CharField(max_length=16, choices=Decision.choices(), default=Decision.NO_ANSWER.value)
    seen = models.BooleanField(null=False, blank=False, default=False)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, null=False, db_constraint=True, on_delete=models.CASCADE,
                             related_name='requests')
    vacancy = models.ForeignKey(Vacancy, null=False, db_constraint=True, on_delete=models.CASCADE,
                                related_name='requests')

    class Meta:
        db_table = 'request'
