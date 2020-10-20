from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

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


class AuthCredentialsSerializers(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
