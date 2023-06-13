from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'events', EventViewSet)
router.register(r'task-states', TaskStateViewSet)
router.register(r'event-tasks', EventTaskViewSet)
router.register(r'event-users', EventUserViewSet)
router.register(r'event-task-reports', EventTaskReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tg-token/', TokenTgView.as_view(), name='tg_token'),
    path('update-tg-id/', UpdateTgIdView.as_view(), name='update-tg-id'),
]
