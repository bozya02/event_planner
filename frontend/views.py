from django.shortcuts import render, redirect, get_object_or_404
from core.models import *
from .forms import LoginForm
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'home.html')


def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('events')
            else:
                error_message = 'Неверное имя пользователя или пароль'
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def events_view(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})


def event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    can_edit = user.groups.filter(name__in=['Менеджер по организации мероприятия', 'Директор']).exists()
    context = {'event': event, 'can_edit': can_edit}
    return render(request, 'event.html', context)
