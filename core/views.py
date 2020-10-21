from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class UniversityListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializer = UniversitySerializer(many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecializationListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializer = SpecializationSerializer(many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
