import requests
import json
from getpass import getpass

BASE_URL = "http://localhost:8000/api"
token = None
user_type = None

# ==============================================================================
# AUTHENTICATION
# ==============================================================================

def register():
    """Register a new member"""
    print("\n=== Member Registration ===")
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
    gender = input("Gender: ")
    
    data = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "gender": gender
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    
    if response.status_code == 201:
        result = response.json()
        global token
        token = result['token']
        print(f"\nRegistration successful!")
        print(f"  User ID: {result['user_id']}")
    else:
        print(f"\nRegistration failed: {response.text}")

def login():
    """Login existing user"""
    print("\n=== User Login ===")
    username = input("Username: ")
    password = getpass("Password: ")
    
    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    
    if response.status_code == 200:
        result = response.json()
        global token, user_type
        token = result['token']
        user_type = result.get('user_type', 'member')
        print(f"\nLogin successful! (Role: {user_type})")
    else:
        print(f"\nLogin failed: {response.text}")

# ==============================================================================
# MEMBER FUNCTIONS (4 operations)
# ==============================================================================

def view_profile():
    """View current member profile - MEMBER OPERATION 2: Profile Management"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/members/me/", headers=headers)
    
    if response.status_code == 200:
        profile = response.json()
        print("\n" + "="*50)
        print("           YOUR PROFILE")
        print("="*50)
        print(f"\n Name: {profile['first_name']} {profile['last_name']}")
        print(f" Email: {profile['email']}")
        print(f" Date of Birth: {profile.get('date_of_birth', 'N/A')}")
        print(f" Gender: {profile.get('gender', 'N/A')}")
        print(f" Phone: {profile.get('phone', 'N/A')}")
        print("\n" + "="*50)
    else:
        print(f"\nFailed: {response.text}")

def update_profile():
    """Update member profile - MEMBER OPERATION 2: Profile Management"""
    if not token:
        print("\n Please login first!")
        return
    
    print("\n=== Update Profile ===")
    print("(Press Enter to keep current value)")
    
    phone = input("Phone: ")
    gender = input("Gender: ")
    email = input("Email: ")
    
    data = {}
    if phone:
        data["phone"] = phone
    if gender:
        data["gender"] = gender
    if email:
        data["email"] = email
    
    if not data:
        print("\n No changes provided.")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.patch(f"{BASE_URL}/members/update_profile/", json=data, headers=headers)
    
    if response.status_code == 200:
        print("\nProfile updated successfully!")
    else:
        print(f"\nFailed: {response.text}")

def view_dashboard():
    """View member dashboard with aggregated data - MEMBER OPERATION 4: Dashboard"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/members/dashboard/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("\n" + "="*50)
        print("           MEMBER DASHBOARD")
        print("="*50)
        
        # Member info
        member = data.get('member', {})
        print(f"\n Member: {member.get('first_name', '')} {member.get('last_name', '')}")
        print(f" Email: {member.get('email', 'N/A')}")
        
        # Active goals
        active_goals = data.get('active_goals', [])
        print(f"\n Active Goals ({len(active_goals)}):")
        if active_goals:
            for goal in active_goals:
                print(f"   - {goal.get('description', 'N/A')}")
        else:
            print("   No active goals")
        
        # Latest health metric
        metric = data.get('latest_health_metric')
        print(f"\n Latest Health Metric:")
        if metric:
            if metric.get('weight_kg'):
                print(f"   Weight: {metric['weight_kg']} kg")
            if metric.get('body_fat_percent'):
                print(f"   Body Fat: {metric['body_fat_percent']}%")
            if metric.get('heart_rate'):
                print(f"   Heart Rate: {metric['heart_rate']} bpm")
        else:
            print("   No health metrics recorded")
        
        # Total records
        print(f"\n Total Health Records: {data.get('total_health_records', 0)}")
        
        print("\n" + "="*50)
    else:
        print(f"\nFailed: {response.text}")

def manage_fitness_goals():
    """Manage fitness goals - MEMBER OPERATION 3: Health History (Goals)"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    
    while True:
        print("\n=== Fitness Goals ===")
        print("[1] View Goals")
        print("[2] Add Goal")
        print("[3] Update Goal")
        print("[4] Delete Goal")
        print("[0] Back")
        
        choice = input("\nChoice: ")
        
        if choice == "1":
            response = requests.get(f"{BASE_URL}/fitness-goals/my_goals/", headers=headers)
            if response.status_code == 200:
                goals = response.json()
                print(f"\n=== Your Goals ({len(goals)}) ===")
                for goal in goals:
                    status = "Active" if goal.get('is_active') else "Inactive"
                    print(f"[{status}] ID: {goal['id']} | {goal['description']}")
                    print(f"    Target: {goal.get('target_deadline', 'No deadline')}")
            else:
                print(f"\nFailed: {response.text}")
        
        elif choice == "2":
            description = input("Goal description: ")
            target_date = input("Target date (YYYY-MM-DD, optional): ")
            target_value = input("Target value (optional): ")
            unit = input("Unit (optional, e.g., kg, lbs): ")
            
            data = {"description": description, "is_active": True}
            if target_date:
                data["target_deadline"] = target_date
            if target_value:
                data["target_value"] = float(target_value)
            if unit:
                data["unit"] = unit
            
            response = requests.post(f"{BASE_URL}/fitness-goals/create_goal/", json=data, headers=headers)
            if response.status_code == 201:
                print("\nGoal added!")
            else:
                print(f"\nFailed: {response.text}")
        
        elif choice == "3":
            goal_id = input("Goal ID to update: ")
            is_active = input("Mark as active? (yes/no): ").lower() == 'yes'
            
            response = requests.patch(f"{BASE_URL}/fitness-goals/{goal_id}/", 
                                     json={"is_active": is_active}, headers=headers)
            if response.status_code == 200:
                print("\nGoal updated!")
            else:
                print(f"\nFailed: {response.text}")
        
        elif choice == "4":
            goal_id = input("Goal ID to delete: ")
            response = requests.delete(f"{BASE_URL}/fitness-goals/{goal_id}/", headers=headers)
            if response.status_code == 204:
                print("\nGoal deleted!")
            else:
                print(f"\nFailed: {response.text}")
        
        elif choice == "0":
            break

def add_health_metric():
    """Log a health metric - MEMBER OPERATION 3: Health History"""
    if not token:
        print("\n Please login first!")
        return
    
    print("\n=== Log Health Metric ===")
    print("(Press Enter to skip a field)")
    
    weight = input("Weight (kg): ")
    height = input("Height (cm): ")
    body_fat = input("Body Fat (%): ")
    heart_rate = input("Resting Heart Rate (bpm): ")
    
    data = {}
    if weight:
        data["weight_kg"] = float(weight)
    if height:
        data["height_cm"] = float(height)
    if body_fat:
        data["body_fat_percent"] = float(body_fat)
    if heart_rate:
        data["heart_rate"] = int(heart_rate)
    
    if not data:
        print("\n No data provided.")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(f"{BASE_URL}/health-metrics/add_metric/", json=data, headers=headers)
    
    if response.status_code == 201:
        print("\nHealth metric logged!")
    else:
        print(f"\nFailed: {response.text}")

def view_health_history():
    """View health history - MEMBER OPERATION 3: Health History"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/health-metrics/my_history/", headers=headers)
    
    if response.status_code == 200:
        metrics = response.json()
        print(f"\n=== Health History ({len(metrics)} records) ===")
        for metric in metrics:
            print(f"\nDate: {metric['recorded_at'][:10]}")
            if metric.get('weight_kg'):
                print(f"  Weight: {metric['weight_kg']} kg")
            if metric.get('height_cm'):
                print(f"  Height: {metric['height_cm']} cm")
            if metric.get('body_fat_percent'):
                print(f"  Body Fat: {metric['body_fat_percent']}%")
            if metric.get('heart_rate'):
                print(f"  Heart Rate: {metric['heart_rate']} bpm")
    else:
        print(f"\nFailed: {response.text}")

# ==============================================================================
# TRAINER FUNCTIONS (2 operations)
# ==============================================================================

def trainer_set_availability():
    """Set trainer availability - TRAINER OPERATION 1: Set Availability"""
    if not token:
        print("\n Please login first!")
        return
    
    print("\n=== Set Availability ===")
    print("Note: The system has a TRIGGER that prevents overlapping availability slots!")
    start_time = input("Start Time (YYYY-MM-DD HH:MM:SS): ")
    end_time = input("End Time (YYYY-MM-DD HH:MM:SS): ")
    
    data = {
        "start_time": start_time,
        "end_time": end_time
    }
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(f"{BASE_URL}/trainers/set_availability/", 
                            json=data, headers=headers)
    
    if response.status_code == 201:
        print("\nAvailability set!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\nFailed: {response.text}")

def trainer_view_schedule():
    """View trainer schedule (availability) - TRAINER OPERATION 2: Schedule View"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/trainers/my_availability/", headers=headers)
    
    if response.status_code == 200:
        slots = response.json()
        print("\n" + "="*50)
        print("           MY SCHEDULE")
        print("="*50)
        
        print(f"\n Availability Slots ({len(slots)}):")
        if slots:
            for slot in slots:
                print(f"  {slot['start_time']} - {slot['end_time']}")
        else:
            print("  No availability slots set")
        
        print("\n" + "="*50)
    else:
        print(f"\nFailed: {response.text}")

# ==============================================================================
# ADMIN/STAFF FUNCTIONS (2 operations)
# ==============================================================================

def staff_book_room():
    """Book a room - ADMIN OPERATION 1: Room Booking"""
    if not token:
        print("\n Please login first!")
        return
    
    print("\n=== Room Booking ===")
    room_id = input("Room ID: ")
    start_time = input("Start Time (YYYY-MM-DD HH:MM:SS): ")
    end_time = input("End Time (YYYY-MM-DD HH:MM:SS): ")
    booking_type = input("Booking Type (class/pt/other): ")
    
    data = {
        "room_id": room_id,
        "start_time": start_time,
        "end_time": end_time,
        "type": booking_type
    }
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(f"{BASE_URL}/staff/book_room/", json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        print("\nRoom booked successfully!")
        data = response.json()
        if 'booking' in data:
            booking = data['booking']
            print(f"  Booking ID: {booking.get('id')}")
            print(f"  Room: {booking.get('room_name')}")
            print(f"  Start: {booking.get('start_time')}")
            print(f"  End: {booking.get('end_time')}")
    else:
        print(f"\nFailed: {response.text}")

def staff_view_rooms():
    """View available rooms - ADMIN OPERATION 1: Room Booking (view)"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/staff/room_availability/", headers=headers)
    
    if response.status_code == 200:
        rooms = response.json()
        print(f"\n=== Rooms ({len(rooms)}) ===")
        for room in rooms:
            print(f"\nID: {room['id']} | {room['name']}")
            print(f"   Capacity: {room['capacity']}")
    else:
        print(f"\nFailed: {response.text}")

def staff_log_maintenance():
    """Log equipment maintenance issue - ADMIN OPERATION 2: Equipment Maintenance"""
    if not token:
        print("\n Please login first!")
        return
    
    print("\n=== Log Maintenance Issue ===")
    equipment_id = input("Equipment ID: ")
    description = input("Issue Description: ")
    
    data = {
        "equipment_id": equipment_id,
        "description": description
    }
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(f"{BASE_URL}/maintenance-tickets/log_issue/", json=data, headers=headers)
    
    if response.status_code == 201:
        print("\nMaintenance issue logged successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\nFailed: {response.text}")

def staff_view_equipment():
    """View all equipment - ADMIN OPERATION 2: Equipment Maintenance (view)"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/equipment/", headers=headers)
    
    if response.status_code == 200:
        equipment = response.json()
        print(f"\n=== Equipment ({len(equipment)}) ===")
        for item in equipment:
            print(f"\nID: {item['id']} | {item['name']}")
            print(f"   Status: {item['status']}")
            print(f"   Room ID: {item.get('room', 'N/A')}")
    else:
        print(f"\nFailed: {response.text}")

def staff_view_maintenance():
    """View maintenance tickets - ADMIN OPERATION 2: Equipment Maintenance (view)"""
    if not token:
        print("\n Please login first!")
        return
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/maintenance-tickets/all_tickets/", headers=headers)
    
    if response.status_code == 200:
        tickets = response.json()
        print(f"\n=== Maintenance Tickets ({len(tickets)}) ===")
        for ticket in tickets:
            print(f"\nTicket ID: {ticket['id']}")
            print(f"   Equipment: {ticket.get('equipment_name', 'N/A')}")
            print(f"   Issue: {ticket['description']}")
            print(f"   Status: {ticket['status'].upper()}")
            print(f"   Reported: {ticket['reported_at'][:10]}")
    else:
        print(f"\nFailed: {response.text}")

def staff_update_ticket():
    """Update maintenance ticket status - ADMIN OPERATION 2: Equipment Maintenance"""
    if not token:
        print("\n Please login first!")
        return
    
    ticket_id = input("\nTicket ID: ")
    print("\nStatus options: open, in_progress, resolved")
    new_status = input("New Status: ")
    
    data = {"status": new_status}
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.patch(f"{BASE_URL}/maintenance-tickets/{ticket_id}/update_status/", 
                             json=data, headers=headers)
    
    if response.status_code == 200:
        print("\nTicket status updated!")
    else:
        print(f"\nFailed: {response.text}")

# ==============================================================================
# MAIN MENU
# ==============================================================================

def main_menu():
    """Display main menu"""
    while True:
        print("\n" + "="*50)
        print("     FITNESS CLUB MANAGEMENT SYSTEM")
        print("     COMP 3005 - Final Project")
        print("="*50)
        
        if token:
            print(f"\n Logged In ({user_type})")
        else:
            print("\n Not Logged In")
        
        print("\n--- Account ---")
        print("[1] Register (Member)")
        print("[2] Login")
        
        if user_type == 'member':
            print("\n--- Member Functions ---")
            print("[3] View Dashboard (uses PostgreSQL VIEW)")
            print("[4] View Profile")
            print("[5] Update Profile")
            print("[6] Manage Fitness Goals")
            print("[7] Log Health Metrics")
            print("[8] View Health History")
            
        elif user_type == 'trainer':
            print("\n--- Trainer Functions ---")
            print("[3] Set Availability (uses TRIGGER to prevent overlap)")
            print("[4] View My Schedule")
            
        elif user_type == 'staff':
            print("\n--- Admin Functions ---")
            print("[3] Book Room")
            print("[4] View Rooms")
            print("[5] View Equipment")
            print("[6] Log Maintenance Issue")
            print("[7] View Maintenance Tickets")
            print("[8] Update Ticket Status")
            
        print("\n[0] Exit")
        print("\n" + "-"*50)
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            login()
        
        # Member options
        elif choice == "3" and user_type == 'member':
            view_dashboard()
        elif choice == "4" and user_type == 'member':
            view_profile()
        elif choice == "5" and user_type == 'member':
            update_profile()
        elif choice == "6" and user_type == 'member':
            manage_fitness_goals()
        elif choice == "7" and user_type == 'member':
            add_health_metric()
        elif choice == "8" and user_type == 'member':
            view_health_history()
        
        # Trainer options
        elif choice == "3" and user_type == 'trainer':
            trainer_set_availability()
        elif choice == "4" and user_type == 'trainer':
            trainer_view_schedule()
        
        # Staff/Admin options
        elif choice == "3" and user_type == 'staff':
            staff_book_room()
        elif choice == "4" and user_type == 'staff':
            staff_view_rooms()
        elif choice == "5" and user_type == 'staff':
            staff_view_equipment()
        elif choice == "6" and user_type == 'staff':
            staff_log_maintenance()
        elif choice == "7" and user_type == 'staff':
            staff_view_maintenance()
        elif choice == "8" and user_type == 'staff':
            staff_update_ticket()
        
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            if not token:
                print("\n Please login first!")
            else:
                print("\n Invalid choice!")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Starting Fitness Club Management CLI...")
    print(f"Connecting to: {BASE_URL}")
    print("="*50)
    main_menu()
