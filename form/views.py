from rest_framework import status
from rest_framework.permissions import AllowAny
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
