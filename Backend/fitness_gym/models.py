# fitness_gym/models.py
from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='member_profile')
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name'], name='member_name_idx')
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MemberDashboardView(models.Model):
    """Database VIEW - aggregates member data for dashboard"""
    member_id = models.IntegerField(primary_key=True)
    member_name = models.CharField(max_length=200)
    email = models.EmailField()
    active_goals_count = models.IntegerField()
    total_goals = models.IntegerField()
    latest_weight_kg = models.FloatField(null=True)
    latest_body_fat = models.FloatField(null=True)
    last_metric_date = models.DateTimeField(null=True)
    total_health_records = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'member_dashboard_view'

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='trainer_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialty = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AdministrativeStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='staff_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"



class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class FitnessGoal(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="goals")
    description = models.CharField(max_length=255)
    target_value = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)  # e.g., "kg", "% body fat"
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    target_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.description}"


class HealthMetric(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="metrics")
    recorded_at = models.DateTimeField(auto_now_add=True)
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    body_fat_percent = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} @ {self.recorded_at}"


class TrainerAvailability(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="availabilities")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.trainer} available {self.start_time} - {self.end_time}"


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name="equipment")
    status = models.CharField(
        max_length=20,
        choices=[("ok", "OK"), ("maintenance", "Maintenance"), ("out_of_order", "Out of order")],
        default="ok",
    )

    def __str__(self):
        return self.name


class RoomBooking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    booked_by = models.ForeignKey(AdministrativeStaff, on_delete=models.SET_NULL, null=True, related_name="room_bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    booking_type = models.CharField(
        max_length=20,
        choices=[("class", "Class"), ("pt", "Personal Training"), ("other", "Other")],
        default="other"
    )
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.name} - {self.start_time} to {self.end_time}"


class MaintenanceTicket(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="tickets")
    reported_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("open", "Open"), ("in_progress", "In Progress"), ("resolved", "Resolved")],
        default="open",
    )

    def __str__(self):
        return f"Ticket for {self.equipment} ({self.status})"
    
