from django.urls import path

from . import api

urlpatterns = [
    path('posts/<slug:post_id>', api.PostsDetailAPIView.as_view()),
    path('posts', api.PostsAPIView.as_view()),
]