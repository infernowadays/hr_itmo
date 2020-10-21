from django.db import models


class University(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        db_table = 'university'


class Specialization(models.Model):
    code = models.CharField(max_length=64, null=False, blank=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    qualification = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        db_table = 'specialization'
