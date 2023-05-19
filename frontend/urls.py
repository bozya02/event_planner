from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_list, name='users_list'),
]
