from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from company import views

urlpatterns = [
    path('projects/', csrf_exempt(views.CompanyListView.as_view())),
    path('projects/<int:pk>/', csrf_exempt(views.CompanyDetailView.as_view())),

]
