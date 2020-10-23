from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from vacancy import views

urlpatterns = [
    path('vacancies/', csrf_exempt(views.VacancyListView.as_view())),
    path('skills/', csrf_exempt(views.SkillListView.as_view())),
]
