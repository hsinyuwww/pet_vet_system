from datetime import datetime

import mysql.connector
import sys

class PetVetSystem:
    def __init__(self):
        """Initialize the system and establish database connection"""
        self.db = None
        self.cursor = None
        self.attempt_connection()

    def attempt_connection(self):
        """
        Attempt to connect to the MySQL database with user credentials.
        """
        while True:
            try:
                username = input("Enter MySQL username: ")
                password = input("Enter MySQL password: ")

                # Attempt to establish connection
                self.db = mysql.connector.connect(
                    host="localhost",
                    user=username,
                    password=password,
                    database="petvet_system",
                    autocommit=True
                )
                self.cursor = self.db.cursor(dictionary=True)
                print("\nDatabase connection successful!")
                return

            except mysql.connector.Error as err:
                if err.errno == 1045:
                    print("\nError: Invalid username or password.")
                    print("Please try again.")
                else:
                    print(f"\nDatabase connection error: {err}")
                    retry = input("Would you like to try again? (y/n): ")
                    if retry.lower() != 'y':
                        print("Exiting program...")
                        sys.exit(1)

    def disconnect(self):
        """
        Safely close the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        print("Database connection closed.")

    def main_menu(self):
        """Display and handle the main menu of the system"""
        try:
            while True:
                print("\n=== PetVet Portal System ===")
                print("1. Owner Portal")
                print("2. Veterinarian Portal")
                print("3. Exit")
                choice = input("Enter choice: ")

                if choice == "1":
                    self.owner_login()
                elif choice == "3":
                    print("Goodbye!")
                    self.disconnect()
                    sys.exit(0)
                else:
                    print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            self.disconnect()
            sys.exit(1)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            self.disconnect()
            sys.exit(1)

    def owner_login(self):
        """Handle owner login process with ID verification"""
        while True:
            print("\n=== Owner Portal Login ===")
            owner_id = input("Enter Owner ID (or 'back' to return): ")

            if owner_id.lower() == 'back':
                return

            try:
                self.cursor.callproc('sp_verify_owner', [int(owner_id)])
                for result in self.cursor.stored_results():
                    owner = result.fetchone()
                    if owner:
                        print(f"\nWelcome, {owner['name']}!")
                        self.owner_menu(owner['owner_id'])
                        return
                print("Owner ID not found.")
            except ValueError:
                print("Please enter a valid number.")

    def owner_menu(self, owner_id):
        """Display and handle owner portal main menu options"""
        while True:
            print("\n=== Owner Portal ===")
            print("1. View My Profile")
            print("2. Manage Pets")
            print("3. Manage Appointments")
            print("4. View Medical Records")
            print("5. Logout")

            choice = input("Enter choice: ")

            if choice == "1":
                self.view_profile(owner_id)
            elif choice == "2":
                self.manage_pets(owner_id)
            elif choice == "3":
                self.manage_appointments(owner_id)
            elif choice == "4":
                self.view_medical_records(owner_id)
            elif choice == "5":
                print("Logging out...")
                return
            else:
                print("Invalid choice. Please try again.")

    def view_profile(self, owner_id):
        """Display owner profile information and handle profile updates"""
        try:
            self.cursor.callproc('sp_get_owner_profile', [owner_id])
            for result in self.cursor.stored_results():
                profile = result.fetchone()
                print("\n=== My Profile ===")
                print(f"Name: {profile['name']}")
                print(f"Email: {profile['email']}")
                print(f"Phone: {profile['phone']}")
                print(f"Address: {profile['address']}")

                while True:
                    choice = input("\n1. Update Profile\n2. Back to Main Menu\nChoice: ")
                    if choice == "1":
                        self.update_profile(owner_id)
                        break
                    elif choice == "2":
                        break
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_profile(self, owner_id):
        """Handle owner profile information updates"""
        print("\n=== Update Profile ===")
        name = input("New name: ")
        email = input("New email: ")
        phone = input("New phone: ")
        address = input("New address: ")

        try:
            self.cursor.callproc('sp_update_owner_profile',
                                 [owner_id, name, email, phone, address])
            self.db.commit()
            print("Profile updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def manage_pets(self, owner_id):
        """Display and handle pet management options"""
        while True:
            print("\n=== Pet Management ===")
            print("1. View All Pets")
            print("2. Add New Pet")
            print("3. Remove Pet")
            print("4. Back to Main Menu")

            choice = input("Enter choice: ")

            if choice == "1":
                self.view_pets(owner_id)
            elif choice == "2":
                self.add_pet(owner_id)
            elif choice == "3":
                self.remove_pet(owner_id)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")

    def view_pets(self, owner_id):
        """Display all pets belonging to the owner"""
        try:
            self.cursor.callproc('sp_get_owner_pets', [owner_id])
            for result in self.cursor.stored_results():
                pets = result.fetchall()
                print("\n=== My Pets ===")
                for pet in pets:
                    print(f"\nPet ID: {pet['pet_id']}")
                    print(f"Name: {pet['name']}")
                    print(f"Age: {pet['age']}")
                    print(f"Gender: {pet['gender']}")
                    print(f"Weight: {pet['weight']}")
                    if pet['last_visit']:
                        print(f"Last Visit: {pet['last_visit']}")
                    print("-" * 30)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def add_pet(self, owner_id):
        """Handle adding a new pet to the system"""
        print("\n=== Add New Pet ===")
        name = input("Pet name: ")
        age = input("Age: ")
        gender = input("Gender (Male/Female/Unknown): ")
        weight = input("Weight (in kg): ")

        try:
            self.cursor.callproc('sp_add_pet',
                                 [owner_id, name, int(age), gender, float(weight)])
            self.db.commit()
            print("Pet added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def remove_pet(self, owner_id):
        """Handle pet removal from the system"""
        print("\n=== Remove Pet ===")
        self.view_pets(owner_id)
        pet_id = input("\nEnter Pet ID to remove: ")

        if input("Are you sure? (yes/no): ").lower() == 'yes':
            try:
                self.cursor.callproc('sp_remove_pet', [owner_id, int(pet_id)])
                self.db.commit()
                print("Pet removed successfully!")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.db.rollback()

    def manage_appointments(self, owner_id):
        """Display and handle appointment management options"""
        while True:
            print("\n=== Appointments ===")
            print("1. View All Appointments")
            print("2. Schedule New Appointment")
            print("3. Cancel Appointment")
            print("4. Back to Main Menu")

            choice = input("Enter choice: ")

            if choice == "1":
                self.view_appointments(owner_id)
            elif choice == "2":
                self.schedule_appointment(owner_id)
            elif choice == "3":
                self.cancel_appointment(owner_id)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")

    def view_appointments(self, owner_id):
        """Display all appointments for the owner"""
        try:
            self.cursor.callproc('sp_get_owner_appointments', [owner_id])
            for result in self.cursor.stored_results():
                appointments = result.fetchall()
                print("\n=== Appointments ===")
                for appt in appointments:
                    print(f"\nAppointment ID: {appt['appointment_id']}")
                    print(f"Status: {appt['appointment_status']}")
                    print(f"Date: {appt['appointment_date']}")
                    print(f"Time: {appt['appoinment_time']}")
                    print(f"Pet: {appt['pet_name']}")
                    print(f"Vet: {appt['vet_name']}")
                    print(f"Service: {appt['service_desc']}")
                    print(f"Cost: ${appt['cost']}")
                    print(f"Payment Status: {appt['payment_status']}")
                    print("-" * 30)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def schedule_appointment(self, owner_id):
        """Handle scheduling new appointments with input validation"""
        while True:
            self.view_pets(owner_id)
            pet_id = input("\nEnter Pet ID: ")

            # Validate pet ID
            self.cursor.execute("SELECT COUNT(*) as count FROM Pet WHERE pet_id = %s AND owner_id = %s",
                                (pet_id, owner_id))
            if self.cursor.fetchone()['count'] == 0:
                print("Error: Invalid Pet ID. Please select a valid pet from the list.")
                continue

            # Display and validate service
            while True:
                self.cursor.execute("SELECT * FROM Service")
                services = self.cursor.fetchall()
                print("\nAvailable Services:")
                for service in services:
                    print(f"{service['service_id']}. {service['description']} - ${service['cost']}")
                service_id = input("Enter Service ID: ")

                # Validate service ID
                self.cursor.execute("SELECT COUNT(*) as count FROM Service WHERE service_id = %s",
                                    (service_id,))
                if self.cursor.fetchone()['count'] == 0:
                    print("Error: Invalid Service ID. Please select a valid service from the list.")
                    continue
                break

            # Display and validate veterinarian
            while True:
                self.cursor.execute("SELECT * FROM Veterinarian")
                vets = self.cursor.fetchall()
                print("\nVeterinarians:")
                for vet in vets:
                    print(f"{vet['vet_id']}. {vet['name']} - {vet['specialization']}")
                vet_id = input("Enter Vet ID: ")

                # Validate vet ID
                self.cursor.execute("SELECT COUNT(*) as count FROM Veterinarian WHERE vet_id = %s",
                                    (vet_id,))
                if self.cursor.fetchone()['count'] == 0:
                    print("Error: Invalid Veterinarian ID. Please select a valid veterinarian from the list.")
                    continue
                break

            date_str = input("Enter date (YYYY-MM-DD): ")
            time_str = input("Enter time (HH:MM): ")

            try:
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    datetime.strptime(time_str, '%H:%M')
                except ValueError:
                    print("Error: Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")
                    continue

                self.cursor.callproc('sp_schedule_appointment',
                                     [owner_id, int(pet_id), int(vet_id),
                                      int(service_id), date_str, time_str])
                self.db.commit()
                print("Appointment scheduled successfully!")
                break
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.db.rollback()
                continue

    def cancel_appointment(self, owner_id):
        """Handle appointment cancellation"""
        self.view_appointments(owner_id)
        appt_id = input("\nEnter Appointment ID to cancel: ")

        try:
            self.cursor.callproc('sp_cancel_appointment', [owner_id, int(appt_id)])
            self.db.commit()
            print("Appointment cancelled successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def view_medical_records(self, owner_id):
        """Display medical records for a selected pet"""
        while True:
            self.view_pets(owner_id)
            pet_id = input("\nEnter Pet ID to view medical records: ")

            # Validate pet ID and ownership
            self.cursor.execute("""
                SELECT COUNT(*) as count 
                FROM Pet 
                WHERE pet_id = %s AND owner_id = %s
            """, (pet_id, owner_id))

            if self.cursor.fetchone()['count'] == 0:
                print("Error: Invalid Pet ID. Please select a valid pet from the list.")
                continue

            try:
                self.cursor.callproc('sp_get_pet_medical_records', [int(pet_id)])
                for result in self.cursor.stored_results():
                    records = result.fetchall()
                    if not records:
                        print("\nNo medical records found for this pet.")
                        break

                    print("\n=== Medical Records ===")
                    for record in records:
                        print(f"\nDate: {record['visit_date']}")
                        print(f"Veterinarian: {record['veterinarian']}")
                        print(f"Specialization: {record['specialization']}")
                        print(f"Diagnosis: {record['diagnosis']}")
                        print(f"Treatment: {record['treatment']}")
                        print(f"Prescriptions: {record['prescriptions']}")
                        print("-" * 30)
                break
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                break


if __name__ == "__main__":
    try:
        system = PetVetSystem()
        system.main_menu()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)