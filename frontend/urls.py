from django.urls import include, path
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('organization/', views.organization_view, name='organization'),
    path('organization/edit/', views.organization_view, name='edit_organization'),
    path('events/', views.events_view, name='events'),
    path('events/<int:event_id>/', views.event_view, name='event'),
    path('events/<int:event_id>/edit/', views.event_view, name='edit_event'),
    path('event/<int:event_id>/add_employees/', views.event_view, name='add_employees'),
    path('events/new/', views.new_event_view, name='new_event'),
    path('reports/', views.reports_view, name='reports'),
    path('employees/', views.employees_view, name='employees'),
    path('employees/<int:employee_id>/', views.employee_view, name='employee'),
    path('employees/<int:employee_id>/edit/', views.employee_view, name='edit_employee'),
    path('employees/new/', views.new_employee_view, name='new_employee'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
