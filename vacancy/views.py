from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from token_auth.enums import Type
from .serializers import *
from .utils import *


class VacancyListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        q = Q() | filter_by_skills(request.GET.get('skill'))
        q = q & filter_by_text(request.GET.get('text'))
        q = q & filter_by_experience_type(request.GET.get('experience_type'))

        if request.GET.get('company'):
            company = Company.objects.filter(pk=request.GET.get('company'))
        else:
            company = {}

        if company:
            q = q & Q(company=company[0])

        vacancies = list(Vacancy.objects.filter(q).distinct().order_by('id'))
        serializer = VacancyShortSerializer(vacancies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.request.user.is_anonymous:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():

            queryset = Company.objects.filter(id=request.data.pop('company_id'))
            if not queryset:
                return Response({'error': 'company not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                company = queryset[0]
            serializer.save(company=company, skills=request.data.get('skills'), jobs=request.data.get('jobs'))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = (AllowAny,)
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

        return Response(setup_single_vacancy_display(serializer.data), status=status.HTTP_200_OK)

    def put(self, request, pk):
        vacancy = self.get_object(pk)
        serializer = VacancySerializer(vacancy, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            company = Company.objects.filter(hr=self.request.user)[0]
            vacancies = VacancyShortSerializer(instance=company.vacancies, many=True)
            for vacancy in vacancies.data:
                responses = list([])

                for request in Request.objects.filter(vacancy_id=vacancy.get('id')):
                    response = dict({})
                    response['vacancy_name'] = vacancy.get('name')
                    response['response_id'] = request.id
                    response['student_id'] = request.user.id
                    response['student_name'] = request.user.first_name + ' ' + request.user.last_name
                    responses.append(response)

                vacancy['responses'] = responses

            responses = vacancies.data

        elif self.request.user.type == Type.STUDENT.value:
            responses = list([])

            for request in Request.objects.filter(user=self.request.user):
                vacancy = Vacancy.objects.get(id=request.vacancy.id)
                company = Company.objects.get(id=vacancy.company.id)

                response = dict({})
                response['vacancy_id'] = vacancy.id
                response['vacancy_name'] = vacancy.name
                response['vacancy_description'] = vacancy.description
                response['vacancy_short_description'] = vacancy.short_description
                response['response_id'] = request.id
                response['response_decision'] = request.decision
                response['response_seen'] = request.seen
                response['company_id'] = company.id
                response['company_logo'] = company.logo
                response['company_name'] = company.name
                responses.append(response)
        else:
            return Response(RequestSerializer(Request.objects.all(), many=True).data, status=status.HTTP_200_OK)

        return Response(responses, status=status.HTTP_200_OK)


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
