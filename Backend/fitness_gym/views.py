from django.shortcuts import render
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class FitnessGoalViewSet(viewsets.ModelViewSet):
    queryset = FitnessGoal.objects.all()
    serializer_class = FitnessGoalSerializer

class HealthMetricViewSet(viewsets.ModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer

class GroupClassViewSet(viewsets.ModelViewSet):
    queryset = GroupClass.objects.all()
    serializer_class = GroupClassSerializer

class ClassSessionViewSet(viewsets.ModelViewSet):
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer

class ClassRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ClassRegistration.objects.all()
    serializer_class = ClassRegistrationSerializer

class PersonalTrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = PersonalTrainingSession.objects.all()
    serializer_class = PersonalTrainingSessionSerializer

class TrainerAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = TrainerAvailability.objects.all()
    serializer_class = TrainerAvailabilitySerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class MaintenanceTicketViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTicket.objects.all()
    serializer_class = MaintenanceTicketSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
