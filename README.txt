Adam Al Gharib - 101234567
COMP 3005 Final Project: Health & Fitness Club Management System

---

**Note:** This README is lengthy because the video presentation time was not enough to cover all technical and demo details. Please refer to this document for a complete understanding of the project.

---

# Project Overview
This is a Health & Fitness Club Management System built for COMP 3005. It uses Django 5.x, Django REST Framework, and PostgreSQL. The system supports three roles: Member, Trainer, and Administrative Staff, with secure token-based authentication and a CLI client for interaction.

## Features & Requirements
- 10 domain entities (Member, Trainer, AdministrativeStaff, Room, Equipment, FitnessGoal, HealthMetric, TrainerAvailability, RoomBooking, MaintenanceTicket)
- 1 VIEW: `member_dashboard_view` (aggregates member data)
- 1 TRIGGER: Prevents overlapping trainer availability slots
- 1 INDEX: On Member (last_name, first_name)
- 8 core operations (4 Member, 2 Trainer, 2 Admin)
- ER diagram included (see project files)

# Setup Instructions

## 1. Prerequisites
- Python 3.11+
- PostgreSQL (running on localhost:5432)
- Git
- Windows OS (tested)

## 2. Clone the Repository
```
git clone <your-github-url>
cd "COMP 3005 Final Project/App"
```

## 3. Create & Activate Virtual Environment
```
python -m venv .venv
.venv\Scripts\activate
```

## 4. Install Dependencies
```
pip install -r requirements.txt
```

## 5. Database Setup
- Create a PostgreSQL database named `fitness_club`.
- Update `Backend/app/settings.py` if your DB credentials differ (default: user `postgres`, no password).
- Run migrations:
```
cd Backend
python manage.py migrate
```

## 6. Run the Server
```
python manage.py runserver
```

## 7. Populate Sample Data
- You can use the following SQL queries in pgAdmin or psql to quickly populate sample data:

```sql
-- Rooms
INSERT INTO fitness_gym_room (name, capacity) VALUES
  ('Studio A', 20),
  ('Studio B', 15),
  ('Yoga Room', 25),
  ('Spin Room', 18),
  ('Weights Room', 30);

-- Equipment
INSERT INTO fitness_gym_equipment (name, type, status) VALUES
  ('Treadmill', 'Cardio', 'available'),
  ('Elliptical', 'Cardio', 'available'),
  ('Bench Press', 'Strength', 'available'),
  ('Rowing Machine', 'Cardio', 'maintenance'),
  ('Dumbbells', 'Strength', 'available');

-- Trainer (assuming user with id=2 exists)
INSERT INTO fitness_gym_trainer (user_id, first_name, last_name, email) VALUES
  (2, 'John', 'Doe', 'trainer1@example.com');

-- Administrative Staff (assuming user with id=3 exists)
INSERT INTO fitness_gym_administrativestaff (user_id, first_name, last_name, email) VALUES
  (3, 'Jane', 'Smith', 'admin1@example.com');
```

Adjust `user_id` values to match your actual user table IDs for trainers and staff. You can create users via Django admin or shell first, then link them here.

## 9. Run the CLI Client
```
cd ..
python main.py
```

# Usage Guide

## Authentication
Register as a member via CLI or use provided demo accounts:
  - Trainer: `trainer1@example.com` / password you set for user id=2
  - Admin: `admin1@example.com` / password you set for user id=3

## Trainer Operations
- Set availability (TRIGGER prevents overlaps)
- View own schedule

## Administrative Staff Operations
- Book rooms (prevents double-booking)
- Log equipment maintenance tickets
- View dashboard (room/equipment/ticket stats)

## Database Features
- **VIEW:** `member_dashboard_view` (aggregates member info)
- **TRIGGER:** Prevents overlapping trainer availability
- **INDEX:** On Member name for fast lookup

## Demo Instructions
- Show TRIGGER: Try to set overlapping trainer availability (see README for test times)
- Show VIEW: Access member dashboard via CLI
- Show INDEX: Query members by name (admin panel or shell)

# Project Structure
- `Backend/fitness_gym/models.py`: All models
- `Backend/fitness_gym/views.py`: API endpoints
- `Backend/fitness_gym/serializers.py`: DRF serializers
- `Backend/fitness_gym/urls.py`: API routing
- `Backend/app/settings.py`: Django settings
- `main.py`: CLI client
- `requirements.txt`: Python dependencies

# Troubleshooting
- If you get a 404, check the URL and ensure the server is running
- If you get a 500 on set availability, it's likely the TRIGGER fired (see error message)
- For DB errors, check PostgreSQL is running and credentials are correct

# ER Diagram
- See attached ER diagram file for entity relationships

# Video Presentation
Paste your video link here:

https://youtu.be/QvN9UHN-kSE

# GitHub Repository
Paste your GitHub repo URL here:

https://github.com/AdamAlGharib/fitness-club-management-system
