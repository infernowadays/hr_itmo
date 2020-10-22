from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .serializers import *
from .models import UserProfile


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
            if not user:
                raise Http404
            token, _ = Token.objects.get_or_create(user=user)

            response = dict({})
            response['token'] = token.key
            response['type'] = request.data.get('type')

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthCredentialsSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        user = authenticate(email=email, password=password)
        if not user:
            raise Http404
        token, _ = Token.objects.get_or_create(user=user)

        response = dict({})
        response['token'] = token.key
        response['type'] = UserProfile.objects.get(email=email).type

        return Response(response, status=status.HTTP_201_CREATED)
