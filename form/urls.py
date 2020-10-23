from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from form import views

urlpatterns = [
    path('forms/', csrf_exempt(views.FormListView.as_view())),
]
