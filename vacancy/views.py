from django.db.models import F
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import *
from .serializers import *
from .utils import *


class VacancyListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        q = Q(is_active=True)
        q = q & filter_by_skills(request.GET.get('skill'))
        q = q & filter_by_text(request.GET.get('text'))
        q = q & filter_by_experience_type(request.GET.get('experience_type'))

        limit = 20
        if request.GET.get('limit'):
            limit = request.GET.get('limit')

        offset = 0
        if request.GET.get('offset'):
            offset = request.GET.get('offset')

        if request.GET.get('is_external') and request.GET.get('is_external') == 'true':
            q = q & Q(is_external=True)
        else:
            q = q & Q(is_external=False)

        if request.GET.get('company'):
            company = Company.objects.filter(pk=request.GET.get('company'))
        else:
            company = {}

        if company:
            q = q & Q(company=company[0])

        vacancies = list(
            Vacancy.objects.filter(q).distinct().order_by('-created')[int(offset): int(offset) + int(limit)])
        serializer = VacancyShortSerializer(vacancies, many=True)

        return Response(setup_vacancy_display(serializer.data), status=status.HTTP_200_OK)

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
            serializer.save(company=company, skills=request.data.get('skills'))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(handle_serializer_errors(Vacancy, serializer.errors), status=status.HTTP_400_BAD_REQUEST,
                        content_type="text/plain")


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
        Vacancy.objects.filter(pk=vacancy.id).update(views=F('views') + 1)

        context = dict({})
        if request.headers.get('Authorization') is not None:
            if vacancy.company.profile.id == self.request.user.id:
                context['is_creator'] = True
            if Request.objects.filter(vacancy=vacancy, user=self.request.user).count() > 0:
                context['is_requested'] = True

        serializer = VacancyShortSerializer(vacancy, context=context)
        return Response(setup_single_vacancy_display(serializer.data), status=status.HTTP_200_OK)

    def put(self, request, pk):
        if request.headers.get('Authorization') is None:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        vacancy = self.get_object(pk)
        serializer = VacancySerializer(vacancy, data=self.request.data, partial=True)
        if serializer.is_valid():

            queryset = Company.objects.filter(id=request.data.pop('company_id'))
            if not queryset:
                return Response({'error': 'company not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                company = queryset[0]
            serializer.save(company=company, skills=request.data.get('skills'))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.headers.get('Authorization') is None:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        vacancy = self.get_object(pk)
        vacancy.is_active = False
        vacancy.save()
        return Response(status=status.HTTP_200_OK)


class RequestListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, vacancy_id=request.data['vacancy_id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        roles = list([])

        company_id = None
        if request.GET.get('id'):
            company_id = request.GET.get('id')

        if not request.GET.getlist('me'):
            roles.append('creator')
            roles.append('member')
        else:
            roles = request.GET.getlist('me')

        responses = list([])

        if company_id is None:
            q = Q()
            q = q & filter_by_request_types(list_roles=roles, user=request.user)
            requests = Request.objects.filter(q)

            for i in range(len(requests)):
                responses.append(self.set_invitations(requests[i]))

        else:
            requests = Request.objects.filter(
                vacancy_id__in=Vacancy.objects.filter(company_id=company_id).values_list('id', flat=True)).distinct()

            for i in range(len(requests)):
                responses.append(self.set_invitations(requests[i]))

        return Response(responses, status=status.HTTP_200_OK)

    @staticmethod
    def set_invitations(request):
        response = dict({})
        response['vacancy_id'] = request.vacancy.id
        response['vacancy_name'] = request.vacancy.name
        response['vacancy_description'] = request.vacancy.description
        response['response_id'] = request.id
        response['response_decision'] = request.decision
        response['response_seen'] = request.seen
        response['company_id'] = request.vacancy.company.id
        response['company_logo'] = request.vacancy.company.logo
        response['company_name'] = request.vacancy.company.name
        response['from_user_id'] = request.user.id
        response['from_user_name'] = request.user.first_name + ' ' + request.user.last_name
        response['from_user_email'] = request.user.email
        response['created'] = request.created

        return response


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

    def delete(self, request, pk):
        request_obj = self.get_object(pk)
        request_obj.delete()
        return Response(status=status.HTTP_200_OK)
