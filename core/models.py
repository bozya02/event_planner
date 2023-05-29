import os
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.deconstruct import deconstructible
from rest_framework_simplejwt.tokens import RefreshToken


@deconstructible
class UniqueUploadName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return self.path % (instance.id, filename)


class Organization(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    tg_id = models.CharField(max_length=30, verbose_name='Id Телеграм', blank=True, null=True)
    organization = models.ForeignKey('Organization', blank=True, null=True,  on_delete=models.CASCADE, verbose_name='Организация')
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Event(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    organization = models.ForeignKey('Organization', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Организация')
    description = models.TextField(max_length=16000, blank=True, null=True, verbose_name='Описание')
    start_date = models.DateTimeField(verbose_name='Дата')
    photo = models.ImageField(upload_to=UniqueUploadName('images/events/'), blank=True,
                              verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Участник мероприятия')

    def __str__(self):
        return f'{self.event} - {self.user}'

    class Meta:
        verbose_name = 'Участник мероприятия'
        verbose_name_plural = 'Участники мероприятий'


class TaskState(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'


class EventTask(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(max_length=16000, blank=True, null=True, verbose_name='Описание')
    event_user = models.ForeignKey(EventUser, on_delete=models.CASCADE, verbose_name='Сотрудник')
    status = models.ForeignKey(TaskState, on_delete=models.CASCADE, verbose_name='Статус')

    def __str__(self):
        return f'{self.name} - {self.event_user}'

    class Meta:
        verbose_name = 'Задача мероприятия'
        verbose_name_plural = 'Задачи мероприятий'


class EventTaskReport(models.Model):
    task = models.ForeignKey(EventTask, on_delete=models.CASCADE, verbose_name='Задание')
    photo = models.ImageField(upload_to=UniqueUploadName('images/event_task_reports/'), blank=True,
                              verbose_name='Изображение')
    message = models.TextField(blank=True, verbose_name='Сообщение')

    def __str__(self):
        return f'{self.task} - {self.pk}'

    class Meta:
        verbose_name = 'Отчет о задаче мероприятия'
        verbose_name_plural = 'Отчеты о задачах мероприятий'
