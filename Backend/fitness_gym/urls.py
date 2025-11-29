from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fitness_gym.views import *

router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')
router.register(r'trainers', TrainerViewSet, basename='trainer')
router.register(r'staff', AdministrativeStaffViewSet, basename='staff')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'fitness-goals', FitnessGoalViewSet, basename='fitnessgoal')
router.register(r'health-metrics', HealthMetricViewSet, basename='healthmetric')
router.register(r'trainer-availabilities', TrainerAvailabilityViewSet, basename='traineravailability')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'maintenance-tickets', MaintenanceTicketViewSet, basename='maintenanceticket')

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name='register'),
    path("api/auth/login/", LoginView.as_view(), name='login'),
]