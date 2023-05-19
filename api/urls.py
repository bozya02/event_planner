from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'task-states', views.TaskStateViewSet)
router.register(r'event-tasks', views.EventTaskViewSet)
router.register(r'event-users', views.EventUserViewSet)
router.register(r'event-task-reports', views.EventTaskReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
