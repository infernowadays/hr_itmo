from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from company.models import Company
from token_auth.enums import *
from vacancy.serializers import VacancySerializer
from vacancy.models import Vacancy


class CompanyListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        if self.request.user.type == Type.ADMINISTRATOR.value:
            companies = CompanyShortSerializer(Company.objects.all(), many=True).data
            for company in companies:
                company['vacancies_count'] = Vacancy.objects.filter(company_id=company.get('id')).count()
            return Response(companies, status=status.HTTP_200_OK)

        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            if self.request.user.type == Type.STUDENT.value:
                return Response({'error': 'student can not create companies'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            elif self.request.user.type == Type.EMPLOYER.value or self.request.user.type == Type.ADMINISTRATOR.value:
                if Company.objects.filter(hr=self.request.user) and self.request.user.type == Type.EMPLOYER.value:
                    return Response({'error': 'user can not create more than one company'},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)

                city = City.objects.filter(id=request.data.get('city'))
                if not city:
                    return Response({'error': 'city does not exists'}, status=status.HTTP_404_NOT_FOUND)

                serializer.save(hr=self.request.user, city=city[0])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        Company.objects.all().delete()
        return Response(status=status.HTTP_200_OK)


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
