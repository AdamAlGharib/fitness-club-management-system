from rest_framework import serializers
from .models import *

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class ClassSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSession
        fields = '__all__'  

class PersonalTrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalTrainingSession
        fields = '__all__'

class GroupClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupClass
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Room
        fields = '__all__'  

class TrainerAvailabilitySerializer(serializers.ModelSerializer):        
    class Meta:
        model = TrainerAvailability
        fields = '__all__'

class ClassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRegistration
        fields = '__all__'

class FitnessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessGoal
        fields = '__all__'

class HealthMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetric
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class MaintenanceTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTicket
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

