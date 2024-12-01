## 2. Owner Portal Access
### Step 1: Login
```
=== Owner Portal Login ===
Enter Owner ID (or 'back' to return): _
Welcome, [Owner Name]!
```

### Step 2: Main Menu Options
```
=== Owner Portal ===
1. View My Profile
2. Manage Pets
3. Manage Appointments
4. View Medical Records
5. Logout
Enter choice: _
```

### Step 3:  Profile Management

View My Profile
```
=== My Profile ===
* Displays:
  - Name
  - Email
  - Phone
  - Address

Options:
1. Update Profile
2. Back to Main Menu Choice: _

// If Update Profile selected:
=== Update Profile ===
-New name: _
-New email: _
-New phone:_
-New address: _
-Profile updated successfully!
```

### Step 4:  Pet Management
=== Pet Management ===
1. View All Pets
2. Add New Pet
3. Remove Pet
4. Back to Main Menu
Enter choice: _

// View Pets Display
=== My Pets ===
Pet ID: [id]
Name: [name]
Age: [age]
Gender: [gender]
Weight: [weight]
Last Visit: [date]
------------------------------

// Add New Pet
=== Add New Pet ===
Pet name: _
Age: _
Gender (Male/Female/Unknown): _
Weight (in kg): _

// Remove Pet
Enter Pet ID to remove: _
Are you sure? (yes/no): _

```

Appointment Management
```
=== Appointments ===
1. View All Appointments
2. Schedule New Appointment
3. Cancel Appointment
4. Back to Main Menu
Enter choice: _

// View Appointments
Display Appointment ID: [id]
Status: [status]
Date: [date]
Time: [time]
Pet: [pet_name]
Vet: [vet_name]
Service: [service_desc]
Cost: $[amount]
Payment Status: [status]
------------------------------

 // Schedule Appointment Process
1. Enter Pet ID: _
2. Select Service ID: _
3. Select Veterinarian ID: _
4. Enter date (YYYY-MM-DD): _
5. Enter time (HH:MM): _

// Cancel Appointment
Enter Appointment ID to cancel: _
```

View Medical Records
```
=== Medical Records ===
Enter Pet ID to view medical records: _

// Display Records
=== Medical Records ===
Date: [visit_date]
Veterinarian: [vet_name]
Specialization: [specialization]
Diagnosis: [diagnosis]
Treatment: [treatment]
Prescriptions: [prescriptions]
------------------------------
```
