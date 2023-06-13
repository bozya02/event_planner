from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from core.models import CustomUser, Event, EventUser, TaskState, EventTask, EventTaskReport


@authentication_classes([])
@permission_classes([])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@authentication_classes([])
@permission_classes([])
class TokenTgView(TokenObtainPairView):
    serializer_class = TgIdSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tg_id = serializer.validated_data['tg_id']

        User = get_user_model()
        try:
            user = User.objects.get(tg_id=tg_id)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid tg_id.'}, status=status.HTTP_400_BAD_REQUEST)

        token = AccessToken.for_user(user)

        return Response({'token': str(token)}, status=status.HTTP_200_OK)


# class CustomTokenObtainPairView(TokenObtainPairSerializer):
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Исполняющий персонал').exists():
            current_time = timezone.now()
            event_user_current = EventUser.objects.filter(user=user, event__start_date__lte=current_time,
                                                          event__end_date__gte=current_time).order_by(
                '-event__start_date').first()
            event_user_future = EventUser.objects.filter(user=user, event__start_date__gt=current_time,
                                                         event__end_date__gte=current_time).order_by(
                'event__start_date').first()

            if event_user_current:
                return event_user_current.eventtask_set.all()
            elif event_user_future:
                return event_user_future.eventtask_set.all()
            else:
                return EventTask.objects.none()
        return EventTask.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class EventTaskReportViewSet(viewsets.ModelViewSet):
    queryset = EventTaskReport.objects.all()
    serializer_class = EventTaskReportSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class UpdateTgIdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tg_id = request.data.get('tg_id')

        if not tg_id:
            return Response({'detail': 'Missing tg_id'}, status=400)

        user = request.user
        user.tg_id = tg_id
        user.save()

        return Response({'detail': 'tg_id updated successfully'}, status=200)
