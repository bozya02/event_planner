from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework.permissions import IsAuthenticated
#
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from .serializers import *
from core.models import CustomUser, Event, EventUser, TaskState, EventTask, EventTaskReport


class ObtainTokenByTgIdView(ObtainAuthToken):
    serializer_class = CustomTokenObtainPairSerializer


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#
#         tg_id = user.tg_id
#
#         try:
#             user = CustomUser.objects.get(tg_id=tg_id)
#         except CustomUser.DoesNotExist:
#             raise exceptions.AuthenticationFailed('Invalid tg_id')
#
#         token = super().get_token(user)
#         return token




class CustomUserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserWriteSerializer


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


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
