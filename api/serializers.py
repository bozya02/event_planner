from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import *


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавьте дополнительные поля пользователя в полезную нагрузку токена (необязательно)
        token['tg_id'] = user.tg_id

        return token


class CustomUserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'tg_id',]


class CustomUserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'token']


class CustomUserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'tg_id', 'email', 'password', 'groups', 'token']
        extra_kwargs = {'tg_id': {'write_only': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            tg_id=validated_data['tg_id'],
        )
        group_names = validated_data.get('groups', [])

        # Назначьте группы пользователю
        groups = Group.objects.filter(name__in=group_names)
        user.groups.set(groups)

        user.set_password(validated_data['password'])
        user.is_staff = True

        user.save()

        return CustomUserTokenSerializer(user).data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


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
