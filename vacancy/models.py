from django.db import models

from company.models import Company
from core.models import Specialization
from token_auth.models import UserProfile
from .enums import *


class Skill(models.Model):
    text = models.CharField(max_length=256, null=False, unique=True)

    class Meta:
        db_table = 'skill'


class Course(models.Model):
    name = models.CharField(max_length=256, null=False, blank=True)
    link = models.CharField(max_length=256, null=False, blank=True)

    class Meta:
        db_table = 'course'


class Vacancy(models.Model):
    name = models.CharField(max_length=128, null=False, blank=True)
    short_description = models.CharField(max_length=256, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    salary = models.IntegerField(null=False, blank=True)

    experience_type = models.IntegerField(null=False, blank=True)
    schedule_type = models.IntegerField(null=False, blank=True)
    employment_type = models.IntegerField(null=False, blank=True)

    approved = models.BooleanField(null=False, blank=False, default=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    skills = models.ManyToManyField(Skill, through='VacancySkills')
    min_points = models.IntegerField(null=True, blank=True, default=0)
    specializations = models.ManyToManyField(Specialization, through='VacancySpecializations')

    external = models.BooleanField(null=False, blank=False, default=False)
    link = models.CharField(max_length=256, null=True, blank=True, default='')

    courses = models.ManyToManyField(Course, through='VacancyCourses')

    company = models.ForeignKey(Company, null=False, db_constraint=True, on_delete=models.CASCADE,
                                related_name='vacancies')

    class Meta:
        db_table = 'vacancy'


class VacancySkills(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'vacancy_skills'
        unique_together = ['vacancy', 'skill']


class VacancySpecializations(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=False)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'vacancy_specializations'
        unique_together = ['vacancy', 'specialization']


class VacancyCourses(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'vacancy_courses'
        unique_together = ['vacancy', 'course']


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
