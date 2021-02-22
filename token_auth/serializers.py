from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer

from .models import UserProfile


class TokenSerializer(ModelSerializer):
    user = UserProfile

    class Meta:
        model = Token
        fields = ['key', 'user', ]


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        profile = UserProfile.objects.create_user(**validated_data)
        return profile

    def to_representation(self, obj):
        profile = super(UserProfileSerializer, self).to_representation(obj)
        profile.pop('password')
        profile.pop('is_active')
        profile.pop('is_admin')
        profile.pop('is_staff')
        profile.pop('is_blocked')
        profile.pop('is_superuser')
        profile.pop('last_login')
        profile.pop('user_permissions')
        profile.pop('groups')

        return profile


class UserProfileShortSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AuthCredentialsSerializers(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class VKOAuthCredentialsSerializers(Serializer):
    email = serializers.EmailField(required=True)
    access_token = serializers.CharField(required=True)
