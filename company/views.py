from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import FileSerializer
from core.utils import *
from vacancy.serializers import VacancySerializer
from .serializers import *


class CompanyListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = CompanySerializer(Company.objects.filter(is_external=False), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.request.user.is_anonymous:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(data=self.request.data)
        if serializer.is_valid():
            city = get_city(self.request.data.get('city'))
            category = get_category(self.request.data.get('category'))

            serializer.save(profile=self.request.user, city=city, category=category)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(handle_serializer_errors(Company, serializer.errors), status=status.HTTP_400_BAD_REQUEST,
                        content_type="text/plain")


class UploadRolePhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadLogoView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()

            company = self.get_object(pk)
            company.logo = file.file
            company.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        serializer_data = serializer.data
        serializer_data['vacancies'] = VacancySerializer(instance=company.vacancies, many=True).data

        serializer_data['is_admin'] = False
        if request.headers.get('Authorization') is not None:
            token = Token.objects.filter(key=request.headers.get('Authorization').replace('Token ', ''))
            if token and token[0].user_id == company.profile.id:
                serializer_data['is_admin'] = True

        return Response(serializer_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if request.headers.get('Authorization') is None:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        company = self.get_object(pk)
        serializer = CompanySerializer(company, data=self.request.data, partial=True)
        if serializer.is_valid():
            city = City.objects.filter(id=self.request.data.get('city'))[0]
            serializer.save(city=city)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.headers.get('Authorization') is None:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_200_OK)
