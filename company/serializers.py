from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import CitySerializer
from token_auth.serializers import UserProfileSerializer
from .models import *


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CompanySerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    roles = RoleSerializer(many=True)
    city = CitySerializer(read_only=True)

    def create(self, validated_data):
        roles = validated_data.pop('roles')

        company = Company.objects.create(**validated_data)

        for role in roles:
            role = Role.objects.create(**role)
            CompanyRoles.objects.create(company=company, role=role)

        return company

    def to_representation(self, obj):
        company = super(CompanySerializer, self).to_representation(obj)
        company.pop('profile')

        return company

    class Meta:
        model = Company
        fields = '__all__'


class CompanyShortSerializer(ModelSerializer):
    profile_first_name = serializers.CharField(source='profile.first_name')
    profile_last_name = serializers.CharField(source='profile.last_name')

    class Meta:
        model = Company
        fields = ('id', 'name', 'profile_first_name', 'profile_last_name',)
