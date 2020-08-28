from django.urls import path
from .views import DeccanApi, FileExists

urlpatterns = [
    path('', DeccanApi.as_view()),
    path('find/', FileExists.as_view())
]
