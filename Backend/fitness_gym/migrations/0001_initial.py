from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Initial migration for Health and Fitness Club Management System
    Creates all tables, the VIEW, TRIGGER, and INDEX
    """

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        # ============================================================
        # ENTITY 1: Member
        # ============================================================
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_profile', to='auth.user')),
            ],
        ),
        
        # ============================================================
        # INDEX on Member (last_name, first_name)
        # Purpose: Speed up member name searches
        # ============================================================
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['last_name', 'first_name'], name='member_name_idx'),
        ),
        
        # ============================================================
        # ENTITY 2: Trainer
        # ============================================================
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('specialty', models.CharField(blank=True, max_length=200)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_profile', to='auth.user')),
            ],
        ),
        
        # ============================================================
        # ENTITY 3: AdministrativeStaff
        # ============================================================
        migrations.CreateModel(
            name='AdministrativeStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('position', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff_profile', to='auth.user')),
            ],
        ),
        
        # ============================================================
        # ENTITY 4: Room
        # ============================================================
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('capacity', models.PositiveIntegerField()),
                ('location', models.CharField(blank=True, max_length=200)),
            ],
        ),
        
        # ============================================================
        # ENTITY 5: Equipment
        # ============================================================
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('ok', 'OK'), ('maintenance', 'Maintenance'), ('out_of_order', 'Out of order')], default='ok', max_length=20)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipment', to='fitness_gym.room')),
            ],
        ),
        
        # ============================================================
        # ENTITY 6: FitnessGoal
        # ============================================================
        migrations.CreateModel(
            name='FitnessGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('target_value', models.FloatField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('target_deadline', models.DateField(blank=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='fitness_gym.member')),
            ],
        ),
        
        # ============================================================
        # ENTITY 7: HealthMetric
        # ============================================================
        migrations.CreateModel(
            name='HealthMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('height_cm', models.FloatField(blank=True, null=True)),
                ('weight_kg', models.FloatField(blank=True, null=True)),
                ('heart_rate', models.IntegerField(blank=True, null=True)),
                ('body_fat_percent', models.FloatField(blank=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='fitness_gym.member')),
            ],
        ),
        
        # ============================================================
        # ENTITY 8: TrainerAvailability
        # ============================================================
        migrations.CreateModel(
            name='TrainerAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='fitness_gym.trainer')),
            ],
        ),
        
        # ============================================================
        # ENTITY 9: RoomBooking
        # ============================================================
        migrations.CreateModel(
            name='RoomBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('booking_type', models.CharField(choices=[('class', 'Class'), ('pt', 'Personal Training'), ('other', 'Other')], default='other', max_length=20)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='fitness_gym.room')),
                ('booked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_bookings', to='fitness_gym.administrativestaff')),
            ],
        ),
        
        # ============================================================
        # ENTITY 10: MaintenanceTicket
        # ============================================================
        migrations.CreateModel(
            name='MaintenanceTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')], default='open', max_length=20)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='fitness_gym.equipment')),
            ],
        ),
        
        # ============================================================
        # DATABASE VIEW: member_dashboard_view
        # Purpose: Aggregate member data for dashboard display
        # ============================================================
        migrations.RunSQL(
            sql="""
                CREATE OR REPLACE VIEW member_dashboard_view AS
                SELECT 
                    m.id AS member_id,
                    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
                    m.email,
                    COUNT(DISTINCT CASE WHEN fg.is_active = TRUE THEN fg.id END) AS active_goals_count,
                    COUNT(DISTINCT fg.id) AS total_goals,
                    (
                        SELECT hm.weight_kg 
                        FROM fitness_gym_healthmetric hm 
                        WHERE hm.member_id = m.id 
                        ORDER BY hm.recorded_at DESC 
                        LIMIT 1
                    ) AS latest_weight_kg,
                    (
                        SELECT hm.body_fat_percent 
                        FROM fitness_gym_healthmetric hm 
                        WHERE hm.member_id = m.id 
                        ORDER BY hm.recorded_at DESC 
                        LIMIT 1
                    ) AS latest_body_fat,
                    (
                        SELECT hm.recorded_at 
                        FROM fitness_gym_healthmetric hm 
                        WHERE hm.member_id = m.id 
                        ORDER BY hm.recorded_at DESC 
                        LIMIT 1
                    ) AS last_metric_date,
                    (
                        SELECT COUNT(*) 
                        FROM fitness_gym_healthmetric hm 
                        WHERE hm.member_id = m.id
                    ) AS total_health_records
                FROM fitness_gym_member m
                LEFT JOIN fitness_gym_fitnessgoal fg ON m.id = fg.member_id
                GROUP BY m.id, m.first_name, m.last_name, m.email;
            """,
            reverse_sql="DROP VIEW IF EXISTS member_dashboard_view;"
        ),
        
        # ============================================================
        # DATABASE TRIGGER: prevent_trainer_availability_overlap
        # Purpose: Prevent trainers from having overlapping availability windows
        # ============================================================
        migrations.RunSQL(
            sql="""
                CREATE OR REPLACE FUNCTION prevent_trainer_availability_overlap()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM fitness_gym_traineravailability
                        WHERE trainer_id = NEW.trainer_id
                        AND id != COALESCE(NEW.id, 0)
                        AND (
                            (NEW.start_time >= start_time AND NEW.start_time < end_time)
                            OR (NEW.end_time > start_time AND NEW.end_time <= end_time)
                            OR (NEW.start_time <= start_time AND NEW.end_time >= end_time)
                        )
                    ) THEN
                        RAISE EXCEPTION 'Trainer already has availability defined for this time slot';
                    END IF;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER check_trainer_availability_overlap
                BEFORE INSERT OR UPDATE ON fitness_gym_traineravailability
                FOR EACH ROW
                EXECUTE FUNCTION prevent_trainer_availability_overlap();
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS check_trainer_availability_overlap ON fitness_gym_traineravailability;
                DROP FUNCTION IF EXISTS prevent_trainer_availability_overlap();
            """
        ),
    ]
