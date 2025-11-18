from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fitness_gym.views import *

router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')
router.register(r'trainers', TrainerViewSet, basename='trainer')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'fitness-goals', FitnessGoalViewSet, basename='fitnessgoal')
router.register(r'health-metrics', HealthMetricViewSet, basename='healthmetric')
router.register(r'group-classes', GroupClassViewSet, basename='groupclass')
router.register(r'class-sessions', ClassSessionViewSet, basename='classsession')
router.register(r'class-registrations', ClassRegistrationViewSet, basename='classregistration')
router.register(r'personal-training-sessions', PersonalTrainingSessionViewSet, basename='personaltrainingsession')
router.register(r'trainer-availabilities', TrainerAvailabilityViewSet, basename='traineravailability')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'maintenance-tickets', MaintenanceTicketViewSet, basename='maintenanceticket')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoiceitem')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path("api/", include(router.urls)),
]