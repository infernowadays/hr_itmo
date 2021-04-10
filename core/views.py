from django.core.mail import EmailMultiAlternatives
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .utils import get_hh_skills


class UniversityListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        universities = University.objects.all()
        serializer = UniversitySerializer(universities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecializationListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SkillListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({'text': get_hh_skills(request.GET.get('text'))}, status=status.HTTP_200_OK)


class LandingListView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(to_email):
        mail_subject = 'Ранний доступ FindFound.me'
        html_content = '''Спасибо за проявленный интерес! Мы будем рады поделиться с тобой новостями об открытии в числе первых!</br></br>
        
        С уважением,</br>
        Администрация FindFound.me
        '''

        email = EmailMultiAlternatives(
            mail_subject,
            html_content,
            to=[to_email]
        )

        email.content_subtype = 'html'
        email.mixed_subtype = 'related'

        email.send()

    def post(self, request):
        serializer = LandingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.send_email(serializer.data.get('email'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
