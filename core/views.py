import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


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
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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

        email.content_subtype = 'html'  # set the primary content to be text/html
        email.mixed_subtype = 'related'  # it is an important part that ensures embedding of an image

        # image_path = settings.STATIC_ROOT + '\\logo.png'
        # image_name = Path(image_path).name
        # if all([html_content, image_path, image_name]):
        #
        #     with open(image_path, mode='rb') as f:
        #         image = MIMEImage(f.read())
        #         email.attach(image)
        #         image.add_header('Content-ID', f"<{image_name}>")

        email.send()

    def post(self, request):
        serializer = LandingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.send_email(serializer.data.get('email'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
