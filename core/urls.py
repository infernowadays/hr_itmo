from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from core import views

urlpatterns = [
    path('universities/', csrf_exempt(views.UniversityListView.as_view())),
    path('specializations/', csrf_exempt(views.SpecializationListView.as_view())),
    path('cities/', csrf_exempt(views.CityListView.as_view())),
    path('skills/', csrf_exempt(views.SkillListView.as_view())),
    path('landing/', csrf_exempt(views.LandingListView.as_view())),
]
