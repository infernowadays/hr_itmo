from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import UserProfile
from core.serializers import SpecializationSerializer
from core.models import Specialization


class TokenSerializer(ModelSerializer):
    user = UserProfile

    class Meta:
        model = Token
        fields = ['key', 'user', ]


class UserProfileSerializer(ModelSerializer):
    specialization = SpecializationSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        specialization = Specialization.objects.get(pk=validated_data.pop('specialization'))
        profile = UserProfile.objects.create_user(**validated_data, specialization=specialization)
        return profile

    def to_representation(self, obj):
        profile = super(UserProfileSerializer, self).to_representation(obj)
        profile.pop('password')
        profile.pop('is_active')
        profile.pop('is_admin')
        profile.pop('is_staff')
        profile.pop('is_superuser')
        profile.pop('last_login')
        profile.pop('user_permissions')
        profile.pop('groups')

        return profile


class UserProfileShortSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'is_filled',)


class AuthCredentialsSerializers(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
