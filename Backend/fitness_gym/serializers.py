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

class AdministrativeStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeStaff
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Room
        fields = '__all__'  

class TrainerAvailabilitySerializer(serializers.ModelSerializer):        
    class Meta:
        model = TrainerAvailability
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

class RoomBookingSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = RoomBooking
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = User
        fields = ['username', 'id', 'password', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract Member-specific fields
        date_of_birth = validated_data.pop('date_of_birth', None)
        gender = validated_data.pop('gender', None)
        
        # Create User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        
        # Create Member profile
        member = Member.objects.create(
            user=user,
            date_of_birth=date_of_birth,
            gender=gender,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user