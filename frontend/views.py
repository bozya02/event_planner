from django.shortcuts import render
from core.models import *


def home(request):
    return render(request, 'home.html')

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})
