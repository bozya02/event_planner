from django.urls import include, path
from rest_framework import routers
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import CustomTokenObtainPairSerializer

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'task-states', views.TaskStateViewSet)
router.register(r'event-tasks', views.EventTaskViewSet)
router.register(r'event-users', views.EventUserViewSet)
router.register(r'event-task-reports', views.EventTaskReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('tg-token/', CustomTokenObtainPairSerializer.as_view(), name='tg_token'),
]
