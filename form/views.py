from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class FormListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.request.user.is_anonymous:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            profile = self.request.user

            serializer.save(profile=profile, educations=self.request.data.get('educations'),
                            skills=self.request.data.get('skills'),
                            jobs=self.request.data.get('jobs'))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return Form.objects.get(pk=pk)
        except Form.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        form = self.get_object(pk)
        serializer = FormSerializer(form)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        form = self.get_object(pk)
        serializer = FormSerializer(form, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save(educations=self.request.data.get('educations'),
                            skills=self.request.data.get('skills'),
                            jobs=self.request.data.get('jobs'))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        form = self.get_object(pk)
        form.delete()
        return Response(status=status.HTTP_200_OK)
