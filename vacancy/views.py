from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from .models import *
from .serializers import *
from .constants import *
from company.models import Company
from .utils import filter_by_skills, filter_by_specializations, setup_vacancy_display
from django.db.models import Q
from token_auth.enums import Type


class VacancyListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        q = Q() | filter_by_skills(request.GET.getlist('skill'))
        q = q & filter_by_specializations(request.GET.getlist('spec'))

        vacancies = Vacancy.objects.filter(q).distinct().order_by('id')
        serializer = VacancySerializer(vacancies, many=True)
        setup_vacancy_display(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            company = Company.objects.filter(hr=self.request.user)
            if not company:
                return Response({'error': 'user does not belong to any company'}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(company=company[0], skills=request.data.get('skills'),
                            specializations=request.data.get('specializations'), courses=request.data.get('courses'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        Vacancy.objects.all().delete()
        return Response(status=status.HTTP_200_OK)


class FavouriteVacancyListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        favourites = VacancyFavorites.objects.filter(user=self.request.user)
        serializer = FavouriteVacancySerializer(favourites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavouriteVacancySerializer(data=self.request.data)
        if serializer.is_valid():
            vacancy = Vacancy.objects.get(pk=self.request.data.get('vacancy'))
            serializer.save(user=self.request.user, vacancy=vacancy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Vacancy.objects.all().delete()
        return Response(status=status.HTTP_200_OK)


class VacancyDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        vacancy = self.get_object(pk)
        serializer = VacancySerializer(vacancy)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SkillListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, vacancy_id=request.data['vacancy'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if self.request.user.type == Type.EMPLOYER.value:
            company = Company.objects.get(hr=self.request.user)
            vacancies_ids = company.vacancies.values_list('id', flat=True)
            requests = Request.objects.filter(vacancy__in=vacancies_ids).order_by('created')
        elif self.request.user.type == Type.STUDENT.value:
            requests = Request.objects.filter(user=self.request.user).order_by('created')
        else:
            return Response({'': ''}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = RequestSerializer(instance=requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RespondRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        request = self.get_object(pk)
        serializer = RequestSerializer(request, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        request = self.get_object(pk)
        serializer = RequestSerializer(request, data={'seen': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
