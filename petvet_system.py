from datetime import datetime

import mysql.connector
import sys
import pandas as pd
from IPython import embed

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
                if choice == "2":
                    self.vet_login()
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
    
    def vet_login(self):
        """Handle vet login process with ID verification"""
        print("\n=== Veterinarian Portal Login ===")
        print("You chose vet protal. Please enter your ID as login credential!")

        vet_id_dict = {}
        try:
            query = "SELECT * FROM Veterinarian"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                vet_id_dict[row['vet_id']] = row['name']
        except mysql.connector.Error as e:
            code, msg = e.args
            print("Error retrieving vet_ids from the database", code, msg)
            return
        while True:
            try:
                vet_id = int(input("Enter your ID: "))
            except:
                print("Please enter a valid number.")
                continue
            if vet_id not in vet_id_dict:
                print("Login Failed. Please try again!")
                continue
            else:
                name = vet_id_dict[vet_id]
                print(f"Login Success! Welcome, {name}")
                self.vet_menu(vet_id)
                return

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
    
    def vet_menu(self, vet_id):
        while True:
            print("Please select one of the following: ")
            print("1. View My Schedule")
            print("2. Search Patients")
            print("3. Medical Records")
            print("4. Update Profile")
            print("5. Logout")
            try:
                vet_selection = int(input("Your choice: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            match vet_selection:
                case 1:
                    self.view_vet_schedule(vet_id)
                case 2:
                    self.search_patient(vet_id)
                case 3:
                    self.manage_medical_records(vet_id)
                case 4:
                    self.manage_profile(vet_id)
                case 5:
                    print("Logging out...")
                    return
                case _:
                    print("Please enter a valid option.")

    def view_vet_schedule(self, vet_id):
        while True:
            print("Pulling up your schedule...")
            print("Please select display method: ")
            print("1. Schedule for today.")
            print("2. Schedule for the next 7 days.")
            print("3. Schedule for specific date.")
            print("4. Main Menu.")
            try:
                schedule_selection = int(input("Your choice: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            match schedule_selection:
                case 1:
                    try:
                        self.cursor.callproc('schedule_view', (vet_id, schedule_selection,"1900-01-01", ))
                        for result in self.cursor.stored_results():
                            rows = result.fetchall()
                            if len(rows) > 0:
                                columns = list(rows[0].keys())

                                df = pd.DataFrame(columns=columns)
                                for row in rows:
                                    df.loc[len(df)] = row
                                print(df)
                            else:
                                print("No appointment today.\n")
                    except mysql.connector.Error as e:
                        code, msg = e.args
                        print("Cannot execute procedure schedule view.", code, msg)
                        break
                case 2:
                    try:
                        self.cursor.callproc('schedule_view', [vet_id, schedule_selection, "1900-01-01"])
                        for result in self.cursor.stored_results():
                            rows = result.fetchall()
                            if len(rows) > 0:
                                columns = list(rows[0].keys())
                                df = pd.DataFrame(columns=columns)
                                for row in rows:
                                    df.loc[len(df)] = row
                                print(df)
                            else:
                                print("No appointment in the following week.\n")
                    except mysql.connector.Error as e:
                        code, msg = e.args
                        print("Cannot execute procedure schedule view.", code, msg)
                        break
                case 3:
                    while True:
                        date = input("Please enter the date in the format of yyyy-mm-dd: ")
                        try:
                            datetime.strptime(date, '%Y-%m-%d')
                        except ValueError:
                            print("Error: Invalid date or time format. Please use YYYY-MM-DD for date.")
                            continue
                        try:
                            self.cursor.callproc('schedule_view', [vet_id, schedule_selection, date])
                            columns = None
                            
                            for result in self.cursor.stored_results():
                                rows = result.fetchall()
                                if len(rows) > 0:
                                    columns = list(rows[0].keys())

                                    df = pd.DataFrame(columns=columns)
                                    for row in rows:
                                        df.loc[len(df)] = row
                                    print(df)
                                else:
                                    print("No appointment in the following week.\n")

                        except mysql.connector.Error as e:
                            code, msg = e.args
                            print("Cannot execute procedure schedule view.", code, msg)
                            break
                        break
                case 4:
                    print("Back to main menu...\n")
                    break

                case _:
                    print("Please enter a valid option!")
    
    def search_patient(self, vet_id):
        while True:
            print("Search patient by pet ID or pet name")
            patient = input("Which patient are you interested in (Press Q to quit): ")

            if patient.upper() == "Q":
                print("Back to main menu...\n")
                break
            try:
                patient = int(patient)
                print("Searching by patient ID...")
                self.cursor.callproc('patient_search', (patient, "None", vet_id, ))
                for result in self.cursor.stored_results():
                    rows = result.fetchall()
                    if len(rows) > 0:
                        columns = list(rows[0].keys())

                        df = pd.DataFrame(columns=columns)
                        for row in rows:
                            df.loc[len(df)] = row
                        print(df)
                    else:
                        print("No patient with this ID is treated by you. \n")
            except:
                print("Searching by patient name...")
                self.cursor.callproc('patient_search', (0, patient, vet_id, ))
                for result in self.cursor.stored_results():
                    rows = result.fetchall()
                    if len(rows) > 0:
                        columns = list(rows[0].keys())

                        df = pd.DataFrame(columns=columns)
                        for row in rows:
                            df.loc[len(df)] = row
                        print(df)
                    else:
                        print("No patient with this name is treated by you. \n")
    
    def manage_medical_records(self, vet_id):
        print("Pulling up medical records...")
        while True:
            print("1. Create new record for a patient.")
            print("2. Search Medical Record.")
            print("3. Update details of a medical record.")
            print("4. Main Menu.\n")
            try:
                mr_selection = int(input("Your choice: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            match mr_selection:
                case 1:
                    while True:
                        try:
                            pet_id = int(input("Please enter the pet ID: "))
                            break
                        except:
                            print("Please enter a valid number.")
                            continue
                    diagnosis = input("Please enter the diagnosis: ")
                    treatment = input("Please enter the treatement: ")
                    self.cursor.callproc("create_new_record", (pet_id, vet_id, diagnosis, treatment,))
                case 2:
                    while True:
                        try:
                            pet_id = int(input("Please enter the pet ID: "))
                            break
                        except ValueError:
                            print("Please enter a valid number.")
                            continue
                    query = f"SELECT * FROM medical_record WHERE vet_id = {vet_id} and pet_id = {pet_id}"
                    self.cursor.execute(query)
                    rows = self.cursor.fetchall()
                    if len(rows) > 0:
                        columns = list(rows[0].keys())

                        df = pd.DataFrame(columns=columns)
                        for row in rows:
                            df.loc[len(df)] = row
                        print(df)
                    else:
                        print("No patient with this ID is treated by you. \n")
                case 3:
                    query = f"SELECT * FROM medical_record WHERE vet_id = {vet_id}"
                    self.cursor.execute(query)
                    rows = self.cursor.fetchall()
                    pets = []
                    if len(rows) > 0:
                        columns = list(rows[0].keys())

                        df = pd.DataFrame(columns=columns)
                        for row in rows:
                            df.loc[len(df)] = row
                            pets.append(row["pet_id"])
                        print(df)
                    else:
                        print("You don't have any medical records on file.")
                        continue
                    print("These are your patient IDs: ", set(pets))
                    while True:
                        try:
                            pet_id = int(input("Which pet's medical record would you like to change? "))
                            break
                        except ValueError:
                            print("Please enter a valid number.")
                            continue
                    if pet_id not in pets:
                        print("This patient is not treated by you.")
                        continue
                    while True:
                        query = f"SELECT * FROM medical_record WHERE vet_id = {vet_id} and pet_id = {pet_id}"
                        self.cursor.execute(query)
                        rows = self.cursor.fetchall()
                        records = []
                        columns = list(rows[0].keys())
                        df = pd.DataFrame(columns=columns)
                        for row in rows:
                            df.loc[len(df)] = row
                            records.append(row["record_id"])
                        print(df)
                        while True:
                            try:
                                record_to_change = int(input("Please enter the record ID you wish to change: "))
                                break
                            except ValueError:
                                print("Please enter a valid number.")
                                continue
                        if record_to_change not in records:
                            print("Please enter a valid record number! \n")
                            continue
                        while True:
                            field_to_change = input("Please enter a field you wish to change (diagnosis, treatment, or both): ")
                            if field_to_change == "diagnosis":
                                new_diag = input("New diagnosis: ")
                                new_treat = ""
                            elif field_to_change == "treatment":
                                new_treat = input("New treatment: ")
                                new_diag = ""
                            elif field_to_change == "both":
                                new_diag = input("New diagnosis: ")
                                new_treat = input("New treatment: ")
                            else:
                                print("Invalid input, please try again.")
                                continue
                            self.cursor.callproc("update_record", (record_to_change, new_diag, new_treat, ))
                            query = f"SELECT * FROM medical_record WHERE pet_id = {pet_id} and vet_id = {vet_id}"
                            self.cursor.execute(query)
                            rows = self.cursor.fetchall()
                            columns = list(rows[0].keys())
                            df = pd.DataFrame(columns=columns)
                            for row in rows:
                                df.loc[len(df)] = row
                            print(df)
                            break
                        break
                case 4:
                    break
                case _:
                    print("Please enter a valid option!")
    
    def manage_profile(self, vet_id):
        print("Here is the current profile info.")
        query = f"SELECT * FROM veterinarian WHERE vet_id = {vet_id}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = list(rows[0].keys())
        df = pd.DataFrame(columns=columns)
        for row in rows:
            df.loc[len(df)] = row
        print(df)
        while True:
            print("What field would you like to change?")
            print("1. Name")
            print("2. Phone")
            print("3. E-mail")
            print("4. Specialization")
            print("5. Exit")
            try:
                mod_selection = int(input("Please select one of the options above: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            match mod_selection:
                case 1:
                    new_name = input("Please enter the new name: ")
                    self.cursor.callproc("update_profile", (vet_id, new_name, "", "", ""))
                case 2:
                    new_phone = input("Please enter your new phone number: ")
                    self.cursor.callproc("update_profile", (vet_id, "", new_phone, "", ""))
                case 3:
                    new_email = input("Please enter your new email address: ")
                    self.cursor.callproc("update_profile", (vet_id, "", "", new_email, ""))
                case 4:
                    new_spec = input("Please enter your new specialization: ")
                    self.cursor.callproc("update_profile", (vet_id, "", "", "", new_spec))
                case 5:
                    print("Exiting update interface...")
                    break
                case _:
                    print("Please enter a valid option!")
                    continue
            query = f"SELECT * FROM veterinarian WHERE vet_id = {vet_id}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            columns = list(rows[0].keys())
            df = pd.DataFrame(columns=columns)
            for row in rows:
                df.loc[len(df)] = row
            print(df)


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