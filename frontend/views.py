import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from core.models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.db.models import Count, Q


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
    organization_employees = event.organization.customuser_set.filter(
        groups__name='Исполняющий персонал'
    ).exclude(
        id__in=event.eventuser_set.values_list('user__id', flat=True)
    )

    task_states = TaskState.objects.all()

    if event.organization != request.user.organization:
        raise PermissionDenied

    form = None

    if request.method == 'POST':
        if 'edit' in request.path and request.user.has_perm('core.change_event'):
            form = EventForm(request.POST, request.FILES, instance=event)
            print(form.errors)
            if form.is_valid():
                form.save()
                return redirect('event', event_id=event.id)
        elif 'add_employees' in request.path:
            employee_ids = request.POST.getlist('employees')
            employees = request.user.organization.customuser_set.filter(id__in=employee_ids)
            for employee in employees:
                EventUser.objects.create(event=event, user=employee)
            return redirect('event', event_id=event.id)
    elif 'edit' in request.path and request.user.has_perm('core.change_event'):
        form = EventForm(instance=event)

    return render(request, 'event.html', {'event': event, 'form': form,
                                          'organization_employees': organization_employees,
                                          'task_states': task_states})


@login_required
@permission_required('core.add_event', raise_exception=True)
def new_event_view(request, event_id=None):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        print(form.errors)
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
    employees = organization.customuser_set.all()
    context = {'employees': employees}
    return render(request, 'employees.html', context)


@login_required
@permission_required('core.view_customuser', raise_exception=True)
def employee_view(request, employee_id):
    employee = get_object_or_404(CustomUser, id=employee_id)
    form = None

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
            user.save()
            return redirect('employees')
    elif 'edit' in request.path and request.user.has_perm('core.change_customuser'):
        form = EmployeeForm(instance=employee)

    if employee.groups.filter(name='Исполняющий персонал').exists():
        task_data = EventTask.objects.filter(event_user__user=employee).values('state__name').annotate(
            count=Count('id'))

        labels = [state['state__name'] for state in task_data]
        counts = [state['count'] for state in task_data]
        colors = {
            'В процессе': 'rgb(13, 202, 240)',
            'Новая': 'rgb(255, 193, 7)',
            'Выполнена': 'rgb(25, 135, 84)',
            'Не выполнена': 'rgb(220, 53, 69)',
        }

        task_data = {
            'labels': labels,
            'datasets': [{
                'label': 'Количество задач',
                'data': counts,
                'backgroundColor': [colors[state] for state in labels],
                'borderColor': 'rgba(255, 255, 255, 1)',
                'borderWidth': 1
            }]
        }
    else:
        task_data = None

    return render(request, 'employee.html', {'employee': employee, 'form': form, 'task_data': task_data})


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


@login_required()
@permission_required('core.view_organization', raise_exception=True)
def organization_view(request):
    organization = request.user.organization
    form = None
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.save()
            return redirect('organization')
    elif 'edit' in request.path and request.user.has_perm('core.change_organization'):
        form = OrganizationForm(instance=organization)

    return render(request, 'organization.html', {'organization': organization, 'form': form})


@login_required
def profile_view(request):
    user = request.user
    organization = user.organization
    is_director = user.groups.filter(name='Директор').exists()
    organization_form = None
    user_form = None

    if request.method == 'POST':
        # Если пользователь является директором, обработайте данные формы информации об организации
        if is_director:
            organization_form = OrganizationForm(request.POST, instance=user.organization)
            if organization_form.is_valid():
                organization_form.save()
                return redirect('profile')
        else:
            organization_form = OrganizationForm(instance=user.organization)
        # Обработайте данные формы личных данных пользователя
        user_form = EmployeeForm(request.POST, instance=user)
        if user_form.is_valid():
            if not is_director:
                groups = user.groups.all()
                print(groups)
                user = user_form.save(commit=False)
                # Сохраняем изменения пользователя
                user.save()
                # Обновляем группы пользователя
                user.groups.set(groups)
            if user_form.cleaned_data['password_changed']:
                user.set_password(user_form.data['password'])

            # Сохраняем изменения в группах
            user.save()
            return redirect('profile')
    elif 'edit' in request.path:
        if is_director:
            organization_form = OrganizationForm(instance=organization)

        initial_data = {
            'groups': user.groups.all()  # Устанавливаем начальное значение для групп пользователя
        }

        user_form = EmployeeForm(instance=user, initial=initial_data)

    return render(request, 'profile.html',
                  {'user': user, 'user_form': user_form,
                   'organization': organization,
                   'organization_form': organization_form,
                   'is_director': is_director})


@login_required
def overview_view(request):
    user = request.user
    organization = request.user.organization

    executing_staff_group = Group.objects.get(name='Исполняющий персонал')
    task_manager_group = Group.objects.get(name='Менеджер по задачам')
    is_executing_staff = executing_staff_group in user.groups.all()
    is_task_manager = task_manager_group in user.groups.all()

    current_time = timezone.now()
    event_user_current = EventUser.objects.filter(user=user,
                                                  event__start_date__lte=current_time,
                                                  event__end_date__gte=current_time).order_by('-event__start_date') \
        .first()
    event_user_future = EventUser.objects.filter(user=user,
                                                 event__start_date__gt=current_time,
                                                 event__end_date__gte=current_time).order_by('event__start_date') \
        .first()

    responsible_tasks_current = Event.objects.filter(responsible_tasks=user, start_date__lte=current_time,
                                                     end_date__gte=current_time).order_by('-start_date').first()
    responsible_tasks_future = Event.objects.filter(responsible_tasks=user,
                                                    start_date__gt=current_time,
                                                    end_date__gte=current_time).order_by('start_date').first()

    events = [event_user_current.event if event_user_current else None,
              event_user_future.event if event_user_future else None,
              responsible_tasks_current, responsible_tasks_future]
    event = min([event for event in events if event],
                key=lambda e: e.start_date if hasattr(e, 'start_date') else current_time) \
        if events.count(None) != len(events) else None

    if not (is_executing_staff or is_task_manager):
        organization_current = Event.objects.filter(organization=organization,
                                                    start_date__lte=current_time,
                                                    end_date__gte=current_time).order_by('-start_date').first()
        organization_future = Event.objects.filter(organization=organization,
                                                   start_date__gt=current_time,
                                                   end_date__gte=current_time).order_by('start_date').first()

        event = organization_current or organization_future

    if request.method == 'POST':
        event_task_form = NewEventTaskForm(data=request.POST, event=event)
        if event_task_form.is_valid():
            event_task = event_task_form.save(commit=False)
            event_task.save()
            return redirect('overview')
    else:
        event_task_form = NewEventTaskForm(event=event)

    event_tasks = EventTask.objects.filter(event_user__event=event)
    event_state = ("Текущее" if event.start_date <= timezone.now() else "Предстоящее") if event else "Печаль"

    context = {'event': event, 'event_task_form': event_task_form, 'event_tasks': event_tasks,
               'event_state': event_state}
    return render(request, 'overview.html', context)
