import pymysql
import pandas as pd

def vet_portal(name):
    username = input("Enter your username: ")
    pword = input('Enter your password: ')
    connection_flag = False
    # Connect to the database
    try:
        connection = pymysql.connect(host='localhost',
                                     user=username,
                                     password=pword,
                                     database=name,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        
        print("Connection Success!")
        connection_flag = True
    except pymysql.Error as e:
        code, msg = e.args
        print("Cannot connect to the database", code, msg)

    while connection_flag:
        print("Please Select from Following by Typing 1, 2, or 3:")
        print("1: Owner Portal")
        print("2: Veterinarian Portal")
        print("3: Disconnect from the database and close the application. ")
        user_selection = input("Enter your choice: ")

        try:
            user_selection = int(user_selection)

            if user_selection > 3 or user_selection < 1:
                print("Number entered is not a valid choice. Try again.")
                continue
        
        except:
            print("Please enter a valid number.")
            continue
        
        if user_selection == 3:
            print("Disconnecting from the database...")
            break

        if user_selection == 2:
            print("You chose vet protal. Please enter your ID as login credential!")
            vet_id = int(input("Enter your ID: "))

            vet_id_dict = {}
            try:
                c1 = connection.cursor()
                query = "SELECT * FROM Veterinarian"
                c1.execute(query)
                for row in c1.fetchall():
                    vet_id_dict[row['vet_id']] = row['name']
                c1.close()
            except pymysql.Error as e:
                code, msg = e.args
                print("Error retrieving vet_ids from the database", code, msg)
                break
            
            if vet_id not in vet_id_dict:
                print("Login Failed. Please try again!")
            else:
                name = vet_id_dict[vet_id]
                print(f"Login Success! Welcome, {name}")
        
            while True:
                
            
                print("Please select one of the following: ")
                print("1. View My Schedule")
                print("2. Search Patients")
                print("3. Medical Records")
                print("4. Update Profile")
                print("5. Logout")

                # We assume the vet will choose an integer number.
                vet_selection = int(input("Your choice: "))
                match vet_selection:
                    case 1:
                        while True:
                            print("Pulling up your schedule...")
                            print("Please select display method: ")
                            print("1. Schedule for today.")
                            print("2. Schedule for the next 7 days.")
                            print("3. Schedule for specific date.")
                            print("4. Main Menu.")
                            schedule_selection = int(input("Your choice: "))
                            match schedule_selection:
                                case 1:
                                    try:
                                        c2 = connection.cursor()
                                        c2.callproc('schedule_view', (vet_id, schedule_selection,"1900-01-01", ))
                                        rows = c2.fetchall()
                                        if len(rows) > 0:
                                            columns = list(rows[0].keys())

                                            df = pd.DataFrame(columns=columns)
                                            for row in rows:
                                                df.loc[len(df)] = row
                                            print(df)
                                        else:
                                            print("No appointment today.\n")
                                        c2.close()
                                    except pymysql.Error as e:
                                        code, msg = e.args
                                        print("Cannot execute procedure schedule view.", code, msg)
                                        break
                                case 2:
                                    try:
                                        c2 = connection.cursor()
                                        c2.callproc('schedule_view', (vet_id, schedule_selection, "1900-01-01", ))
                                        rows = c2.fetchall()
                                        if len(rows) > 0:
                                            columns = list(rows[0].keys())

                                            df = pd.DataFrame(columns=columns)
                                            for row in rows:
                                                df.loc[len(df)] = row
                                            print(df)
                                        else:
                                            print("No appointment in the following week.\n")
                                        c2.close()
                                    except pymysql.Error as e:
                                        code, msg = e.args
                                        print("Cannot execute procedure schedule view.", code, msg)
                                        break
                                case 3:
                                    date = input("Please enter the date in the format of yyyy-mm-dd: ")
                                    try:
                                        c2 = connection.cursor()
                                        c2.callproc('schedule_view', (vet_id, schedule_selection, date, ))
                                        rows = c2.fetchall()
                                        if len(rows) > 0:
                                            columns = list(rows[0].keys())

                                            df = pd.DataFrame(columns=columns)
                                            for row in rows:
                                                df.loc[len(df)] = row
                                            print(df)
                                        else:
                                            print("No appointment on this day.")
                                        c2.close()
                                    except pymysql.Error as e:
                                        code, msg = e.args
                                        print("Cannot execute procedure schedule view.", code, msg)
                                        break
                                case 4:
                                    print("Back to main menu...\n")
                                    break
                    case 2:
                        while True:
                            print("Search patient by pet ID or pet name")
                            patient = input("Which patient are you interested in (Press Q to quit): ")

                            if patient.upper() == "Q":
                                print("Back to main menu...\n")
                                break
                            try:
                                patient = int(patient)
                                print("Searching by patient ID...")
                                c3 = connection.cursor()
                                c3.callproc('patient_search', (patient, "None", vet_id, ))
                                rows = c3.fetchall()
                                if len(rows) > 0:
                                    columns = list(rows[0].keys())

                                    df = pd.DataFrame(columns=columns)
                                    for row in rows:
                                        df.loc[len(df)] = row
                                    print(df)
                                else:
                                    print("No patient with this ID is treated by you. \n")
                                c3.close()
                            except:
                                print("Searching by patient name...")
                                c3 = connection.cursor()
                                c3.callproc('patient_search', (0, patient, vet_id, ))
                                rows = c3.fetchall()
                                if len(rows) > 0:
                                    columns = list(rows[0].keys())

                                    df = pd.DataFrame(columns=columns)
                                    for row in rows:
                                        df.loc[len(df)] = row
                                    print(df)
                                else:
                                    print("No patient with this name is treated by you. \n")
                                c3.close()

                    case 3:
                        print("Pulling up medical records...")
                        while True:
                            print("1. Create new record for a patient.")
                            print("2. Search Medical Record.")
                            print("3. Update details of a medical record.")
                            print("4. Main Menu.\n")
                            mr_selection = int(input("Your choice: "))
                            match mr_selection:
                                case 1:
                                    pet_id = int(input("Please enter the pet ID: "))
                                    diagnosis = input("Please enter the diagnosis: ")
                                    treatment = input("Please enter the treatement: ")

                                    c4 = connection.cursor()
                                    c4.callproc("create_new_record", (pet_id, vet_id, diagnosis, treatment,))
                                    c4.close()

                                case 2:
                                    pet_id = int(input("Please enter the pet ID: "))
                                    c5 = connection.cursor()
                                    query = f"SELECT * FROM medical_record WHERE vet_id = {vet_id} and pet_id = {pet_id}"
                                    c5.execute(query)
                                    rows = c5.fetchall()
                                    if len(rows) > 0:
                                        columns = list(rows[0].keys())

                                        df = pd.DataFrame(columns=columns)
                                        for row in rows:
                                            df.loc[len(df)] = row
                                        print(df)
                                    else:
                                        print("No patient with this ID is treated by you. \n")
                                    c5.close()
                                case 3:
                                    
                                    c6 = connection.cursor()
                                    query = f"SELECT * FROM medical_record WHERE vet_id = {vet_id}"
                                    c6.execute(query)
                                    rows = c6.fetchall()
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
                                    c6.close()
                                    print("These are your patient IDs: ", set(pets))
                                    pet_id = int(input("Which pet's medical record would you like to change? "))
                                    if pet_id not in pets:
                                        print("This patient is not treated by you.")
                                        continue

                                    while True:
                                        c7 = connection.cursor()
                                        query = f"SELECT * FROM medical_record WHERE vet_id = {vet_id} and pet_id = {pet_id}"
                                        c7.execute(query)
                                        rows = c7.fetchall()
                                        records = []
                                        
                                        columns = list(rows[0].keys())

                                        df = pd.DataFrame(columns=columns)
                                        for row in rows:
                                            df.loc[len(df)] = row
                                            records.append(row["record_id"])
                                        print(df)
                                        c7.close()
                                        record_to_change = int(input("Please enter the record ID you wish to change: "))
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
                                            c7 = connection.cursor()
                                            c7.callproc("update_record", (record_to_change, new_diag, new_treat, ))
                                            c7.close()
                                            c6 = connection.cursor()
                                            query = f"SELECT * FROM medical_record WHERE pet_id = {pet_id} and vet_id = {vet_id}"
                                            c6.execute(query)
                                            rows = c6.fetchall()
                                            columns = list(rows[0].keys())

                                            df = pd.DataFrame(columns=columns)
                                            for row in rows:
                                                df.loc[len(df)] = row
                                            print(df)
                                            c6.close()
                                            break
                                        break
                                case 4:
                                    break

                    case 4:
                        print("Here is the current profile info.")
                        query = f"SELECT * FROM veterinarian WHERE vet_id = {vet_id}"
                        c8 = connection.cursor()
                        c8.execute(query)
                        rows = c8.fetchall()
                        columns = list(rows[0].keys())

                        df = pd.DataFrame(columns=columns)
                        for row in rows:
                            df.loc[len(df)] = row
                        print(df)
                        c8.close()
                        while True:
                            print("What field would you like to change?")
                            print("1. Name")
                            print("2. Phone")
                            print("3. E-mail")
                            print("4. Specialization")
                            print("5. Exit")
                            mod_selection = int(input("Please select one of the options above: "))

                            match mod_selection:
                                case 1:
                                    new_name = input("Please enter the new name: ")
                                    c9 = connection.cursor()
                                    c9.callproc("update_profile", (vet_id, new_name, "", "", ""))
                                    c9.close()
                                case 2:
                                    new_phone = input("Please enter your new phone number: ")
                                    c9 = connection.cursor()
                                    c9.callproc("update_profile", (vet_id, "", new_phone, "", ""))
                                    c9.close()
                                case 3:
                                    new_email = input("Please enter your new email address: ")
                                    c9 = connection.cursor()
                                    c9.callproc("update_profile", (vet_id, "", "", new_email, ""))
                                    c9.close()
                                case 4:
                                    new_spec = input("Please enter your new specialization: ")
                                    c9 = connection.cursor()
                                    c9.callproc("update_profile", (vet_id, "", "", "", new_spec))
                                    c9.close()
                                case 5:
                                    print("Exiting update interface...")
                                    break
                                case _:
                                    print("Please enter a valid option!")
                                    continue

                            query = f"SELECT * FROM veterinarian WHERE vet_id = {vet_id}"
                            c8 = connection.cursor()
                            c8.execute(query)
                            rows = c8.fetchall()
                            columns = list(rows[0].keys())

                            df = pd.DataFrame(columns=columns)
                            for row in rows:
                                df.loc[len(df)] = row
                            print(df)
                            c8.close()

                    case _:
                        print("Exiting vet portal... \n")
                        break

            
            


    connection.close()

if __name__ == '__main__':
    vet_portal('petvet_system')

