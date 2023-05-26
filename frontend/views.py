from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
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


@login_required
def events_view(request):
    organization_events = Event.objects.filter(organization=request.user.organization)
    context = {
        'events': organization_events
    }
    return render(request, 'events.html', context)


@login_required
@permission_required('core.view_event', raise_exception=True)
def event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = None

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event', event_id=event.id)
    elif 'edit' in request.path and request.user.has_perm('core.change_event'):
        form = EventForm(instance=event)

    return render(request, 'event.html', {'event': event, 'form': form})


@permission_required('core.add_event', raise_exception=True)
@login_required
def new_event_view(request, event_id=None):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            return redirect('event', event_id=event.id)
    else:
        form = EventForm()

    return render(request, 'new_event.html', {'form': form})


@login_required
def reports_view(request):
    return render(request, 'reports.html')


@login_required
def employees_view(request):
    organization = request.user.organization
    employees = CustomUser.objects.filter(organization=organization)
    context = {'employees': employees}
    return render(request, 'employees.html', context)
