from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from core.models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group


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

            user.groups.add(Group.objects.get(name='Директор'))

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

    if event.organization != request.user.organization:
        raise PermissionDenied

    form = None

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event', event_id=event.id)
    elif 'edit' in request.path and request.user.has_perm('core.change_event'):
        form = EventForm(instance=event)

    return render(request, 'event.html', {'event': event, 'form': form})


@login_required
@permission_required('core.add_event', raise_exception=True)
def new_event_view(request, event_id=None):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organization = request.user.organization
            event.save()
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


@login_required
@permission_required('core.view_customuser', raise_exception=True)
def employee_view(request, employee_id):
    employee = get_object_or_404(CustomUser, id=employee_id)

    if employee.organization != request.user.organization:
        raise PermissionDenied

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            user = form.save(commit=False)
            groups = form.cleaned_data.get('groups')
            if form.cleaned_data['password_changed']:
                user.set_password(form.data['password'])
            user.groups.set(groups)
            print(form.cleaned_data)
            user.save()
            return redirect('employees')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee.html', {'form': form})


@login_required
@permission_required('core.add_customuser', raise_exception=True)
def new_employee_view(request):
    if request.method == 'POST':
        form = NewEmployeeForm(request.POST, request.FILES)
        organization = request.user.organization
        if form.is_valid():
            user = form.save(commit=False)
            groups = form.cleaned_data.get('groups')
            user.organization = organization

            user.save()
            user.groups.set(groups)
            user.save()
            return redirect('employees')
    else:
        form = NewEmployeeForm()

    return render(request, 'new_employee.html', {'form': form})
