from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import *
from token_auth.serializers import UserProfileSerializer
from core.serializers import CitySerializer


class CompanySerializer(ModelSerializer):
    hr = UserProfileSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class CompanyShortSerializer(ModelSerializer):
    hr_first_name = serializers.CharField(source='hr.first_name')
    hr_last_name = serializers.CharField(source='hr.last_name')

    class Meta:
        model = Company
        fields = ('id', 'name', 'hr_first_name', 'hr_last_name',)
