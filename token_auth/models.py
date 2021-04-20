from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.contrib.auth.models import User
from django.db import models

from core.models import Specialization
from .enums import *


class UserProfileManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, sex, photo=None, password=None):
        photo = '' if photo is None else photo

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            sex=sex,
            photo=photo
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth='1900-01-01',
            sex='',
            photo=''
        )

        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=64, unique=True)
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    sex = models.CharField(null=False, blank=False, max_length=16, choices=Sex.choices())
    photo = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
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
