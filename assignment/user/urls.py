from django.urls import path

from . import api

urlpatterns = [
    path('signup', api.SignupAPIView.as_view()),
    path('login', api.LoginAPIView.as_view()),
    path('refresh', api.RefreshAPIView.as_view()),
    path('logout', api.LogoutAPIView.as_view()),
]