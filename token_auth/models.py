import datetime
import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.contrib.auth.models import User
from django.db import models
from .enums import *


class UserProfileManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, university_id, student_id_type, student_id, type, date_of_birth,
                    sex, specialization, degree, course, password):
        if not email or not first_name or not last_name or not university_id or not student_id_type or not student_id \
                or not type or not date_of_birth or not sex or not specialization or not degree or not course:
            raise ValueError("Provide all the data")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            university_id=university_id,
            student_id_type=student_id_type,
            student_id=student_id,
            type=type,
            date_of_birth=date_of_birth,
            sex=sex,
            specialization=specialization,
            degree=degree,
            course=course
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            university_id=university_id,
            student_id_type=student_id_type,
            student_id=student_id,
            type=type,
            date_of_birth=date_of_birth,
            sex=sex,
            specialization=specialization,
            degree=degree,
            course=course
        )

        user.set_password(password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    university_id = models.CharField(max_length=64, null=True, blank=True)
    student_id_type = models.CharField(max_length=16, choices=StudentIdType.choices(),
                                       default=StudentIdType.DIPLOMA.value, blank=True)
    student_id = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=16, choices=Type.choices(), default=Type.STUDENT.value, blank=False)
    degree = models.CharField(max_length=16, choices=Degree.choices(), default=Degree.BACHELOR.value, blank=True)
    date_of_birth = models.DateField(null=False, blank=False)
    sex = models.CharField(max_length=16, choices=Sex.choices(), default=Sex.MALE.value, blank=False)
    course = models.IntegerField(blank=True, default=1)
    specialization = models.IntegerField(blank=True, default=1)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_filled = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = UserProfileManager()

    class Meta:
        db_table = 'user_profile'


class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users_groups'
