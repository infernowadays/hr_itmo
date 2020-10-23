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
