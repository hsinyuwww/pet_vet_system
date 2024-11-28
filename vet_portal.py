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
            print("2. Manage Patients")
            print("3. Medical Records")
            print("4. Update Profile")
            print("5. Logout")

            # We assume the vet will choose an integer number.
            vet_selection = int(input("Your choice: "))
            match vet_selection:
                case 1:
                    print("Pulling up your schedule...")
                    print("Please select display method: ")
                    print("1. Schedule for today.")
                    print("2. Schedule for the next 7 days.")
                    print("3. Full schedule.")
                    schedule_selection = int(input("Your choice: "))
                    match schedule_selection:
                        case 1:
                            try:
                                c2 = connection.cursor()
                                c2.callproc('schedule_view', (vet_id, schedule_selection,))
                                rows = c2.fetchall()
                                if len(rows) > 0:
                                    columns = list(rows[0].keys())

                                    df = pd.DataFrame(columns=columns)
                                    for row in rows:
                                        df.loc[len(df)] = row
                                    print(df)
                                else:
                                    print("No appointment today.")
                                c2.close()
                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Cannot execute procedure schedule view.", code, msg)
                                break
                        case 2:
                            try:
                                c2 = connection.cursor()
                                c2.callproc('schedule_view', (vet_id, schedule_selection,))
                                rows = c2.fetchall()
                                if len(rows) > 0:
                                    columns = list(rows[0].keys())

                                    df = pd.DataFrame(columns=columns)
                                    for row in rows:
                                        df.loc[len(df)] = row
                                    print(df)
                                else:
                                    print("No appointment today.")
                                c2.close()
                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Cannot execute procedure schedule view.", code, msg)
                                break
                        case 3:
                            try:
                                c2 = connection.cursor()
                                c2.callproc('schedule_view', (vet_id, schedule_selection,))
                                rows = c2.fetchall()
                                if len(rows) > 0:
                                    columns = list(rows[0].keys())

                                    df = pd.DataFrame(columns=columns)
                                    for row in rows:
                                        df.loc[len(df)] = row
                                    print(df)
                                else:
                                    print("No appointment today.")
                                c2.close()
                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Cannot execute procedure schedule view.", code, msg)
                                break
                case 2:
                    print("Search patient by pet ID, pet name, or owner name")
                case 3:
                    print("Pulling up medical records...")
                case 4:
                    print("Here is the current profile info.")
                case _:
                    break

            
            


    connection.close()

if __name__ == '__main__':
    vet_portal('petvet_system')

