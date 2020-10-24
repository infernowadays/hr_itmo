from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .models import *
from core.models import University


class FormListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():

            if request.GET.get('student') and self.request.user.type == Type.ADMINISTRATOR.value:
                student = UserProfile.objects.get(pk=request.GET.get('student'))
            else:
                student = self.request.user

            serializer.save(student=student, educations=self.request.data.get('educations'),
                            extra_skills=self.request.data.get('extra_skills'),
                            soft_skills=self.request.data.get('soft_skills'),
                            achievements=self.request.data.get('achievements'),
                            jobs=self.request.data.get('jobs'))

            UserProfile.objects.filter(id=student.id).update(is_filled=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        Form.objects.all().delete()
        return Response(status=status.HTTP_200_OK)
