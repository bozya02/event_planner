from rest_framework import serializers
from core.models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'tg_id']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = '__all__'


class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = '__all__'


class EventTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTask
        fields = '__all__'


class EventTaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTaskReport
        fields = '__all__'
