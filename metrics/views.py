from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import Company
from form.models import Form
from token_auth.enums import Type
from vacancy.enums import Decision
from vacancy.models import Vacancy, Request


class MetricsListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        if self.request.user.type != Type.ADMINISTRATOR.value:
            return Response({'error': 'user is not an administrator'}, status=status.HTTP_403_FORBIDDEN)

        metrics = dict({})
        metrics['forms_total'] = Form.objects.all().count()
        metrics['vacancies_total'] = Vacancy.objects.all().count()
        metrics['companies_total'] = Company.objects.all().count()
        metrics['requests_total'] = Request.objects.count()
        metrics['requests_success'] = Request.objects.filter(decision=Decision.ACCEPT.value).count()

        return Response(metrics, status=status.HTTP_200_OK)
