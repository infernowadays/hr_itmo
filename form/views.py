from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


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
            profile = self.request.user

            serializer.save(profile=profile, educations=self.request.data.get('educations'),
                            skills=self.request.data.get('skills'),
                            jobs=self.request.data.get('jobs'))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
