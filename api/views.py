from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from core.models import CustomUser, Event, EventUser, TaskState, EventTask, EventTaskReport


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserWriteSerializer
        return CustomUserReadSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventUserViewSet(viewsets.ModelViewSet):
    queryset = EventUser.objects.all()
    serializer_class = EventUserSerializer


class TaskStateViewSet(viewsets.ModelViewSet):
    queryset = TaskState.objects.all()
    serializer_class = TaskStateSerializer


class EventTaskViewSet(viewsets.ModelViewSet):
    queryset = EventTask.objects.all()
    serializer_class = EventTaskSerializer


class EventTaskReportViewSet(viewsets.ModelViewSet):
    queryset = EventTaskReport.objects.all()
    serializer_class = EventTaskReportSerializer
