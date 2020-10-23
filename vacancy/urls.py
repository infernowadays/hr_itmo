from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from vacancy import views

urlpatterns = [
    path('vacancies/', csrf_exempt(views.VacancyListView.as_view())),
    path('skills/', csrf_exempt(views.SkillListView.as_view())),
    path('requests/', csrf_exempt(views.RequestListView.as_view())),
    path('requests/<int:pk>/', csrf_exempt(views.RespondRequestView.as_view())),
]
