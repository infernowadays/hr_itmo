from django.urls import path

from . import views

urlpatterns = [
    path('auth', views.auth, name='auth'),
    path('registration', views.registration, name='registration'),
    path('projects', views.projects, name='projects'),
    path('departments', views.departments, name='departments'),
    path('vacancies', views.vacancies, name='vacancies'),
    path('participants', views.participants, name='participants'),
    path('companies', views.companies, name='companies'),
    path('upload_photo', views.upload_photo, name='upload_photo'),
    path('profile', views.profile, name='profile'),

]
