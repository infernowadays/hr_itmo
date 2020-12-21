import datetime
import os

from django.db import models


class University(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)

    class Meta:
        db_table = 'university'


class Specialization(models.Model):
    code = models.CharField(max_length=64, null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    qualification = models.CharField(max_length=128, null=False, blank=False)

    class Meta:
        db_table = 'specialization'


class City(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)

    class Meta:
        db_table = 'city'


class Skill(models.Model):
    text = models.CharField(max_length=256, null=False, unique=True)

    class Meta:
        db_table = 'skill'


class Duty(models.Model):
    text = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'duty'


class Job(models.Model):
    duration = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    duties = models.ManyToManyField(Duty, through='JobDuties')

    class Meta:
        db_table = 'job'


class JobDuties(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'job_duties'


class Landing(models.Model):
    email = models.EmailField(verbose_name='email', max_length=64, null=False, blank=False)
    status = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        db_table = 'landing'


def get_path_for_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(datetime.datetime.now(), ext)
    return os.path.join(filename)


class File(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_path_for_file)

    class Meta:
        db_table = 'file'
