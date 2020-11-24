from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from vacancy.serializers import VacancySerializer
from .serializers import *


class CompanyListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = CompanySerializer(Company.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.request.user.is_anonymous:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(data=self.request.data)
        if serializer.is_valid():
            city = City.objects.filter(id=self.request.data.get('city'))[0]
            serializer.save(profile=self.request.user, city=city)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    permission_classes = (IsAuthenticated,)
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
        return Response(serializer_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanySerializer(company, data=self.request.data, partial=True)
        if serializer.is_valid():
            city = City.objects.filter(id=self.request.data.get('city'))[0]
            serializer.save(city=city)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_200_OK)
