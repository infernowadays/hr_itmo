from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from metrics import views

urlpatterns = [
    path('metrics/', csrf_exempt(views.MetricsListView.as_view())),
]
