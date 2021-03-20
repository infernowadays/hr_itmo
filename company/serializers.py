from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import CitySerializer
from token_auth.serializers import UserProfileSerializer
from .models import *
from .utils import create_company_roles


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
        create_company_roles(company, roles)

        return company

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles')

        if roles is not None:
            create_company_roles(instance, roles)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.city = validated_data.get('city', instance.city)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.state = validated_data.get('state', instance.state)
        instance.link = validated_data.get('link', instance.link)

        instance.save()

        return instance

    def to_representation(self, obj):
        company = super(CompanySerializer, self).to_representation(obj)
        company.pop('profile')

        return company

    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {
            "name": {"error_messages": {"required": "название"}},
            "description": {"error_messages": {"required": "описание"}},
            "subject": {"error_messages": {"required": "отрасль"}},
            "state": {"error_messages": {"required": "стадия"}},
        }


class CompanyShortSerializer(ModelSerializer):
    profile_first_name = serializers.CharField(source='profile.first_name')
    profile_last_name = serializers.CharField(source='profile.last_name')

    class Meta:
        model = Company
        fields = ('id', 'name', 'profile_first_name', 'profile_last_name',)
