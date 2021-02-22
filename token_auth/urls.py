from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from token_auth import views

urlpatterns = [
    path('auth/', csrf_exempt(views.LoginView.as_view())),
    path('users/', csrf_exempt(views.SignUpView.as_view())),
    path('users/me/', csrf_exempt(views.MyProfileView.as_view())),
    path('users/<int:pk>/photo/', csrf_exempt(views.UploadPhotoView.as_view())),
    path('auth/vk/', csrf_exempt(views.OAuthVKView.as_view())),
    path('auth/vk/code/', csrf_exempt(views.GetAccessTokenView.as_view())),
]
