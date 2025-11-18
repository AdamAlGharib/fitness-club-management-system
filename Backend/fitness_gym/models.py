# fitness_gym/models.py
from django.db import models


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender        = models.CharField(max_length=20, null=True, blank=True)
    phone         = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Trainer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    specialty  = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Room(models.Model):
    name       = models.CharField(max_length=100, unique=True)
    capacity   = models.PositiveIntegerField()
    location   = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class FitnessGoal(models.Model):
    member         = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="goals")
    description    = models.CharField(max_length=255)
    target_value   = models.FloatField(null=True, blank=True)
    unit           = models.CharField(max_length=50, blank=True)  # e.g., "kg", "% body fat"
    is_active      = models.BooleanField(default=True) 
    created_at     = models.DateTimeField(auto_now_add=True)
    target_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.description}"


class HealthMetric(models.Model):
    member     = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="metrics")
    recorded_at = models.DateTimeField(auto_now_add=True)
    height_cm  = models.FloatField(null=True, blank=True)
    weight_kg  = models.FloatField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    body_fat_percent = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} @ {self.recorded_at}"


class GroupClass(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ClassSession(models.Model):
    group_class = models.ForeignKey(GroupClass, on_delete=models.CASCADE, related_name="sessions")
    trainer     = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, related_name="class_sessions")
    room        = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="class_sessions")
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    capacity    = models.PositiveIntegerField()

    attendees   = models.ManyToManyField(Member, through="ClassRegistration", related_name="class_sessions")

    def __str__(self):
        return f"{self.group_class.name} on {self.start_time}"


class ClassRegistration(models.Model):
    member       = models.ForeignKey(Member, on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("member", "class_session")  # prevent duplicate registrations


class PersonalTrainingSession(models.Model):
    member     = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="pt_sessions")
    trainer    = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="pt_sessions")
    room       = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="pt_sessions")
    start_time = models.DateTimeField()
    end_time   = models.DateTimeField()
    status     = models.CharField(
        max_length=20,
        choices=[("scheduled", "Scheduled"), ("completed", "Completed"), ("cancelled", "Cancelled")],
        default="scheduled",
    )

    def __str__(self):
        return f"PT {self.member} with {self.trainer} at {self.start_time}"


class TrainerAvailability(models.Model):
    trainer    = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="availabilities")
    start_time = models.DateTimeField()
    end_time   = models.DateTimeField()

    def __str__(self):
        return f"{self.trainer} available {self.start_time} - {self.end_time}"


class Equipment(models.Model):
    name      = models.CharField(max_length=100)
    room      = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name="equipment")
    status    = models.CharField(
        max_length=20,
        choices=[("ok", "OK"), ("maintenance", "Maintenance"), ("out_of_order", "Out of order")],
        default="ok",
    )

    def __str__(self):
        return self.name


class MaintenanceTicket(models.Model):
    equipment  = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="tickets")
    reported_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status      = models.CharField(
        max_length=20,
        choices=[("open", "Open"), ("in_progress", "In Progress"), ("resolved", "Resolved")],
        default="open",
    )

    def __str__(self):
        return f"Ticket for {self.equipment} ({self.status})"


class Invoice(models.Model):
    member      = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="invoices")
    created_at  = models.DateTimeField(auto_now_add=True)
    due_date    = models.DateField(null=True, blank=True)
    is_paid     = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} for {self.member}"


class InvoiceItem(models.Model):
    invoice     = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    invoice     = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    paid_at     = models.DateTimeField(auto_now_add=True)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    method      = models.CharField(max_length=30)  # "cash", "credit", "debit", etc
