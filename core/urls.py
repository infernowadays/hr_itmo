from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from core import views

urlpatterns = [
    path('universities/', csrf_exempt(views.UniversityListView.as_view())),
    path('specializations/', csrf_exempt(views.SpecializationListView.as_view())),
]
