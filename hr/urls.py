from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('token_auth.urls')),
    path('api/', include('core.urls')),
    path('api/', include('vacancy.urls')),
    path('api/', include('company.urls')),
    path('api/', include('form.urls')),
    path('api/', include('metrics.urls')),
]
