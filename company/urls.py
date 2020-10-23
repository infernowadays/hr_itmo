from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from company import views

urlpatterns = [
    path('companies/', csrf_exempt(views.CompanyListView.as_view())),
]
