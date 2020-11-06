from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from vacancy import views

urlpatterns = [
    path('vacancies/', csrf_exempt(views.VacancyListView.as_view())),
    path('vacancies/<int:pk>/', csrf_exempt(views.VacancyDetailView.as_view())),

    path('favouriteVacancies/', csrf_exempt(views.FavouriteVacancyListView.as_view())),

    path('invitations/', csrf_exempt(views.RequestListView.as_view())),
    path('invitations/<int:pk>/', csrf_exempt(views.RespondRequestView.as_view())),
]
