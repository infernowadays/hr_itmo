from django.db import models
from token_auth.models import UserProfile
from core.models import City


class Company(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    inn = models.CharField(max_length=32, null=False, blank=True)
    ogrn = models.CharField(max_length=32, null=False, blank=True)

    city = models.ForeignKey(City, null=False, db_constraint=True, on_delete=models.CASCADE,
                             related_name='companies')

    address = models.CharField(max_length=256, null=False, blank=True)
    email = models.EmailField(null=False, blank=True)
    phone = models.CharField(max_length=32, null=False, blank=True)
    takes_on_practice = models.BooleanField(max_length=256, null=False, blank=True, default=False)
    logo = models.TextField(null=False, blank=True)
    hr = models.ForeignKey(UserProfile, null=False, db_constraint=True, on_delete=models.CASCADE,
                           related_name='companies')

    class Meta:
        db_table = 'company'
