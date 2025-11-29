from django.shortcuts import render
from django.urls import path, include
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                
                # Determine user type
                user_type = "unknown"
                if hasattr(user, 'member_profile'):
                    user_type = "member"
                elif hasattr(user, 'trainer_profile'):
                    user_type = "trainer"
                elif hasattr(user, 'staff_profile'):
                    user_type = "staff"
                elif user.is_superuser:
                    user_type = "admin"
                
                return Response({
                    "token": token.key,
                    "user_id": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "user_type": user_type
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current logged-in member's profile"""
        try:
            member = request.user.member_profile
            serializer = self.get_serializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({"error": "Member profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """Update current logged-in member's profile"""
        try:
            member = request.user.member_profile
            serializer = self.get_serializer(member, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            return Response({"error": "Member profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def dashboard(self, request):
        """Get member dashboard with stats and goals"""
        try:
            member = request.user.member_profile
            
            # Latest health metrics
            latest_metric = member.metrics.order_by('-recorded_at').first()
            latest_metric_data = HealthMetricSerializer(latest_metric).data if latest_metric else None
            
            # Active fitness goals
            active_goals = member.goals.filter(is_active=True)
            active_goals_data = FitnessGoalSerializer(active_goals, many=True).data
            
            # Health metrics count
            total_metrics = member.metrics.count()
            
            return Response({
                "member": MemberSerializer(member).data,
                "latest_health_metric": latest_metric_data,
                "active_goals": active_goals_data,
                "total_health_records": total_metrics
            })
        except Member.DoesNotExist:
            return Response({"error": "Member profile not found"}, status=status.HTTP_404_NOT_FOUND)


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def dashboard(self, request):
        """Get trainer dashboard"""
        try:
            trainer = request.user.trainer_profile
            
            # Get availability slots
            availability = TrainerAvailability.objects.filter(
                trainer=trainer,
                end_time__gte=timezone.now()
            ).order_by('start_time')[:5]
            availability_data = TrainerAvailabilitySerializer(availability, many=True).data
            
            return Response({
                "trainer": TrainerSerializer(trainer).data,
                "upcoming_availability": availability_data
            })
        except Trainer.DoesNotExist:
            return Response({"error": "Trainer profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a trainer"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_availability(self, request):
        """Set trainer availability - prevents overlapping time windows (via DB trigger)"""
        try:
            trainer = request.user.trainer_profile
            
            data = request.data.copy()
            data['trainer'] = trainer.id
            serializer = TrainerAvailabilitySerializer(data=data)
            
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    # Catch database trigger errors (overlapping availability)
                    error_message = str(e)
                    if 'overlapping' in error_message.lower() or 'overlap' in error_message.lower():
                        return Response({
                            "error": "TRIGGER FIRED: Cannot create overlapping availability slot for this trainer!"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Trainer.DoesNotExist:
            return Response({"error": "Trainer profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a trainer"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_availability(self, request):
        """Get trainer's availability slots"""
        try:
            trainer = request.user.trainer_profile
            availability = TrainerAvailability.objects.filter(
                trainer=trainer
            ).order_by('start_time')
            serializer = TrainerAvailabilitySerializer(availability, many=True)
            return Response(serializer.data)
        except Trainer.DoesNotExist:
            return Response({"error": "Trainer profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a trainer"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def schedule_view(self, request):
        """See all availability slots (Schedule View)"""
        try:
            trainer = request.user.trainer_profile
            
            # All availability slots
            availability = TrainerAvailability.objects.filter(
                trainer=trainer
            ).order_by('start_time')
            availability_data = TrainerAvailabilitySerializer(availability, many=True).data
            
            return Response({
                "availability_slots": availability_data
            })
        except Trainer.DoesNotExist:
            return Response({"error": "Trainer profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a trainer"}, status=status.HTTP_400_BAD_REQUEST)


class AdministrativeStaffViewSet(viewsets.ModelViewSet):
    queryset = AdministrativeStaff.objects.all()
    serializer_class = AdministrativeStaffSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def dashboard(self, request):
        """Get staff dashboard with maintenance tickets and room status"""
        try:
            staff = request.user.staff_profile
            
            # Open maintenance tickets
            open_tickets = MaintenanceTicket.objects.filter(status='open').count()
            in_progress_tickets = MaintenanceTicket.objects.filter(status='in_progress').count()
            
            # Room status
            total_rooms = Room.objects.count()
            
            # Equipment status
            equipment_maintenance = Equipment.objects.filter(status='maintenance').count()
            equipment_out_of_order = Equipment.objects.filter(status='out_of_order').count()
            
            return Response({
                "staff": AdministrativeStaffSerializer(staff).data,
                "maintenance_tickets": {
                    "open": open_tickets,
                    "in_progress": in_progress_tickets
                },
                "room_stats": {
                    "total_rooms": total_rooms
                },
                "equipment_stats": {
                    "maintenance": equipment_maintenance,
                    "out_of_order": equipment_out_of_order
                }
            })
        except AdministrativeStaff.DoesNotExist:
            return Response({"error": "Staff profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a staff member"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def book_room(self, request):
        """Assign room for session or class - prevents double-booking"""
        try:
            staff = request.user.staff_profile
            room_id = request.data.get('room_id')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')
            booking_type = request.data.get('type', 'other')
            description = request.data.get('description', '')
            
            # Check if room exists
            try:
                room = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Check for double-booking
            conflicting_bookings = RoomBooking.objects.filter(
                room_id=room_id,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            if conflicting_bookings.exists():
                return Response({
                    "error": "Room is already booked for this time period"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the booking
            booking = RoomBooking.objects.create(
                room=room,
                booked_by=staff,
                start_time=start_time,
                end_time=end_time,
                booking_type=booking_type,
                description=description
            )
            
            serializer = RoomBookingSerializer(booking)
            return Response({
                "message": "Room booked successfully!",
                "booking": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except AdministrativeStaff.DoesNotExist:
            return Response({"error": "Staff profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a staff member"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def room_availability(self, request):
        """Check room availability"""
        try:
            staff = request.user.staff_profile
            rooms = Room.objects.all()
            return Response(RoomSerializer(rooms, many=True).data)
        except AdministrativeStaff.DoesNotExist:
            return Response({"error": "Staff profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a staff member"}, status=status.HTTP_400_BAD_REQUEST)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FitnessGoalViewSet(viewsets.ModelViewSet):
    queryset = FitnessGoal.objects.all()
    serializer_class = FitnessGoalSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_goals(self, request):
        """Get fitness goals for the logged-in member"""
        try:
            member = request.user.member_profile
            goals = FitnessGoal.objects.filter(member=member).order_by('-created_at')
            serializer = self.get_serializer(goals, many=True)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({"error": "Member profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def create_goal(self, request):
        """Create a fitness goal for the logged-in member"""
        try:
            member = request.user.member_profile
            data = request.data.copy()
            data['member'] = member.id
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            return Response({"error": "Member profile not found"}, status=status.HTTP_404_NOT_FOUND)


class HealthMetricViewSet(viewsets.ModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_history(self, request):
        """Get health metric history for the logged-in member (time-stamped entries)"""
        try:
            member = request.user.member_profile
            metrics = HealthMetric.objects.filter(member=member).order_by('-recorded_at')
            serializer = self.get_serializer(metrics, many=True)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({"error": "Member profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_metric(self, request):
        """Add a new health metric entry for the logged-in member (does NOT overwrite)"""
        try:
            member = request.user.member_profile
            data = request.data.copy()
            data['member'] = member.id
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            return Response({"error": "Member profile not found"}, status=status.HTTP_404_NOT_FOUND)


class TrainerAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = TrainerAvailability.objects.all()
    serializer_class = TrainerAvailabilitySerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class MaintenanceTicketViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTicket.objects.all()
    serializer_class = MaintenanceTicketSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def log_issue(self, request):
        """Log a new equipment maintenance issue"""
        try:
            staff = request.user.staff_profile
            equipment_id = request.data.get('equipment_id')
            description = request.data.get('description')
            
            # Update equipment status to maintenance
            equipment = Equipment.objects.get(id=equipment_id)
            equipment.status = 'maintenance'
            equipment.save()
            
            # Create maintenance ticket
            ticket = MaintenanceTicket.objects.create(
                equipment=equipment,
                description=description,
                status='open'
            )
            
            return Response(MaintenanceTicketSerializer(ticket).data, status=status.HTTP_201_CREATED)
            
        except Equipment.DoesNotExist:
            return Response({"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND)
        except AdministrativeStaff.DoesNotExist:
            return Response({"error": "Staff profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a staff member"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """Update maintenance ticket status"""
        try:
            staff = request.user.staff_profile
            ticket = self.get_object()
            new_status = request.data.get('status')
            
            if new_status not in ['open', 'in_progress', 'resolved']:
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
            
            ticket.status = new_status
            ticket.save()
            
            # If resolved, update equipment status back to ok
            if new_status == 'resolved':
                equipment = ticket.equipment
                equipment.status = 'ok'
                equipment.save()
            
            return Response(MaintenanceTicketSerializer(ticket).data)
            
        except AdministrativeStaff.DoesNotExist:
            return Response({"error": "Staff profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a staff member"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def all_tickets(self, request):
        """Get all maintenance tickets with equipment and room info"""
        try:
            staff = request.user.staff_profile
            tickets = MaintenanceTicket.objects.all().select_related('equipment', 'equipment__room').order_by('-reported_at')
            
            results = []
            for ticket in tickets:
                ticket_data = MaintenanceTicketSerializer(ticket).data
                ticket_data['equipment_name'] = ticket.equipment.name
                ticket_data['room_name'] = ticket.equipment.room.name if ticket.equipment.room else 'N/A'
                results.append(ticket_data)
            
            return Response(results)
            
        except AdministrativeStaff.DoesNotExist:
            return Response({"error": "Staff profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User is not a staff member"}, status=status.HTTP_400_BAD_REQUEST)
