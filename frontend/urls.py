from django.urls import include, path
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('events/', views.events_view, name='events'),
    path('events/<int:event_id>/', views.event_view, name='event'),
    path('reports/', views.reports_view, name='reports'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
