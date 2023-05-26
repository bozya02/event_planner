from django.shortcuts import render, redirect, get_object_or_404
from core.models import *
from .forms import *
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('events')
    else:
        login_form = LoginForm()

    return render(request, 'login.html', {'login_form': login_form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        organization_form = OrganizationForm(request.POST)
        if form.is_valid() and organization_form.is_valid():
            user = form.save(commit=False)
            user.save()

            organization = organization_form.save()
            user.organization = organization
            user.save()

            return redirect('login')
    else:
        form = RegistrationForm()
        organization_form = OrganizationForm()

    return render(request, 'registration.html', {'form': form, 'organization_form': organization_form})


def events_view(request):
    organization_events = Event.objects.filter(organization=request.user.organization)
    context = {
        'events': organization_events
    }
    return render(request, 'events.html', context)


def event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    can_edit = user.groups.filter(name__in=['Менеджер по организации мероприятия', 'Директор']).exists()
    context = {'event': event, 'can_edit': can_edit}
    return render(request, 'event.html', context)


def new_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organization = request.user.organization
            event.save()
            return redirect('events')
    else:
        form = EventCreationForm()

    return render(request, 'new_event.html', {'form': form})

def reports_view(request):
    return render(request, 'reports.html')
