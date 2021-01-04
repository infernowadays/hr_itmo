from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import Company
from company.serializers import CompanySerializer
from form.models import Form
from form.serializers import FormSerializer
from .serializers import *


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

            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
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

        return Response({'token': token.key}, status=status.HTTP_200_OK)


class MyProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializer = UserProfileSerializer(self.request.user)
        serializer_data = serializer.data

        form = Form.objects.filter(profile=self.request.user).order_by('-id')
        serializer_data['form'] = {} if not form else FormSerializer(form[0]).data

        companies = Company.objects.filter(profile=self.request.user)
        serializer_data['companies'] = [] if not companies else CompanySerializer(instance=companies, many=True).data

        return Response(serializer_data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileSerializer(instance=self.request.user, data=self.request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
