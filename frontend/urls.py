from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('events/', views.events_view, name='events'),
    path('events/<int:event_id>/', views.event_view, name='event')
]
